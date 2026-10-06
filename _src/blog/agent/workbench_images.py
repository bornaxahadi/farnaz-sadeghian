# Journal image helper for the Composio remote workbench (COMPOSIO_REMOTE_WORKBENCH).
# Paste this whole file into one workbench cell, then call make_post_images(...) in the next cell.
# Why the workbench: the routine's own sandbox can only reach GitHub, while the workbench can
# reach Higgsfield (gpt-image-2) and download the result. Images land on the `blog-assets`
# branch under incoming/; the agent then copies them into _src/blog/img and blog/img.
# Cost: about 2 Higgsfield credits per image (gpt_image_2, quality medium, 2k).
import base64, io, json, requests
from PIL import Image

REPO = 'bornaxahadi/farnaz-sadeghian'

def _gh(method, path, body=None):
    r, e = proxy_execute(method, f'/repos/{REPO}{path}', 'github', body=body)
    if e:
        raise RuntimeError(f'{method} {path}: {e}')
    return r.get('data', r) if isinstance(r, dict) and 'data' in r and 'status' in r else r

def push_files(files, branch='blog-assets', message='Journal images', folder='incoming/'):
    """One commit with all files on `branch` (created from main if missing)."""
    try:
        head = _gh('GET', f'/git/ref/heads/{branch}')['object']['sha']
    except RuntimeError:
        head = _gh('GET', '/git/ref/heads/main')['object']['sha']
        _gh('POST', '/git/refs', {'ref': f'refs/heads/{branch}', 'sha': head})
    base_tree = _gh('GET', f'/git/commits/{head}')['tree']['sha']
    tree = []
    for name, data in files.items():
        blob = _gh('POST', '/git/blobs', {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
        tree.append({'path': folder + name, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
    t = _gh('POST', '/git/trees', {'base_tree': base_tree, 'tree': tree})
    c = _gh('POST', '/git/commits', {'message': message, 'tree': t['sha'], 'parents': [head]})
    _gh('PATCH', f'/git/refs/heads/{branch}', {'sha': c['sha']})
    return c['sha']

def _variants(im, name):
    W, H = im.size                       # centre-crop to 3:2
    if W / H > 1.5:
        nw = int(H * 1.5); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    elif W / H < 1.5:
        nh = int(W / 1.5); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    out = {}
    for w in (480, 800, 1536):
        b = io.BytesIO(); im.resize((w, round(w / 1.5)), Image.LANCZOS).save(b, 'WEBP', quality=80, method=6)
        out[f'{name}-{w}.webp'] = b.getvalue()
    b = io.BytesIO(); im.resize((1200, 800), Image.LANCZOS).save(b, 'JPEG', quality=84, optimize=True, progressive=True)
    out[f'{name}-og.jpg'] = b.getvalue()
    return out

def generate(prompts):
    """prompts: {image_name: prompt}. Returns {image_name: result_url}."""
    names = list(prompts)
    reqs = [{'index': i, 'params': {'model': 'gpt_image_2', 'prompt': prompts[n], 'aspect_ratio': '3:2',
                                    'quality': 'medium', 'resolution': '2k', 'use_unlim': False}} for i, n in enumerate(names)]
    r, e = run_composio_tool('HIGGSFIELD_MCP_GENERATE_IMAGE_BATCH', {'requests': reqs})
    if e:
        raise RuntimeError(e)
    jobs = [{'index': j['index'], 'job_id': j['job_id']} for j in r['data']['jobs']]
    for _ in range(10):                  # ~150 s max; call generate again in a new cell if it times out
        r, e = run_composio_tool('HIGGSFIELD_MCP_JOBS_WAIT', {'jobs': jobs, 'timeout_seconds': 15})
        if e:
            raise RuntimeError(e)
        if r['data'].get('all_terminal'):
            break
    urls = {}
    for j in r['data']['jobs']:
        if j.get('status') == 'completed' and j.get('result_url'):
            urls[names[j['index']]] = j['result_url']
    return urls

def make_post_images(prompts, message='Journal images'):
    """Generate, resize to the journal's 4 sizes, and push to blog-assets/incoming/. Returns file names."""
    urls = generate(prompts)
    files = {}
    for name, url in urls.items():
        im = Image.open(io.BytesIO(requests.get(url, timeout=60).content)).convert('RGB')
        files.update(_variants(im, name))
    if files:
        push_files(files, message=message)
    return sorted(files), sorted(set(prompts) - set(urls))
