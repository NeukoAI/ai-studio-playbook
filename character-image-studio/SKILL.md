---
name: character-image-studio
description: Manage character visual identities. Create characters, build reference libraries from seed images and turnaround variations, and generate consistent images on demand via the NeukoAI Character Image Studio API.
metadata: {"neuko": {"emoji": "🎨", "homepage": "https://api-imagegen.neuko.ai"}}
---

# Character Image Studio Skill

**Purpose:** Manage your characters' visual identities. Create multiple characters, build reference libraries, and generate consistent images of any character on demand.

**Use when:**
- User needs to create a new character and its reference images
- User wants to generate new images of an existing character
- User wants to manage multiple characters

**Don't use when:** User is asking about something unrelated to visual content generation.

---

## Preflight: Required Setup

**CRITICAL: Complete these steps before using this skill.**

### 1. Image Size Safety

Most LLM providers reject images over 5MB. If an oversized image enters your session, it gets stuck in the conversation history and causes every subsequent message to fail. This bricks the session until you run `/new`.

**Required gateway config** (add to `openclaw.json`):
```json
{
  "agents": {
    "defaults": {
      "mediaMaxMb": 4
    }
  }
}
```
This makes the gateway auto-compress inbound images to stay under 4MB, well within the 5MB API limit. **Without this setting, images sent directly in chat can permanently brick your session.** Apply with `openclaw gateway restart` after editing config.

### 2. Image Compression Protocol

Even with the config above, always follow this protocol for images you handle directly:

**Before reading ANY image** (user uploads, generated outputs, reference images):

1. Save the image to disk first (don't read inline if possible)
2. Check file size:
   ```bash
   FILE_SIZE=$(stat -f%z "image.png" 2>/dev/null || stat -c%s "image.png" 2>/dev/null)
   echo "$FILE_SIZE bytes"
   ```
3. If over 4MB (4194304 bytes), compress before reading:
   ```bash
   # macOS
   sips --resampleHeightWidthMax 2048 --setProperty format jpeg --setProperty formatOptions 75 "input.png" --out "input-compressed.jpg"

   # Linux (ffmpeg - most universal)
   ffmpeg -i "input.png" -vf "scale='min(2048,iw)':'min(2048,ih)':force_original_aspect_ratio=decrease" -q:v 8 "input-compressed.jpg" -y

   # Linux (ImageMagick fallback)
   convert "input.png" -resize 2048x2048\> -quality 75 "input-compressed.jpg"
   ```
4. Use the compressed version for all subsequent operations
5. Store compressed versions in the workspace, not originals

### 3. Image Delivery Capability

This skill regularly sends generated images directly in chat. The user's messaging platform **must** support agent-initiated file/image sends.

**Before starting any workflow, verify:**

1. Check which channel you're in (Slack, Telegram, Discord, etc.)
2. Attempt a test image send or confirm the channel has file upload configured
3. If image sending is NOT available:
   - **Stop.** Do not proceed with the skill.
   - Tell the user: "This skill needs to send images directly in our chat. Your current setup doesn't support that yet. Here's how to enable it:"
   - Guide them through setup for their platform (Slack bot token with `files:write` scope, Telegram bot file sending, etc.)
   - Only proceed after image delivery is confirmed working

**This is not optional.** The entire workflow depends on showing images in chat for review and approval. Falling back to "check the folder" is not acceptable for this skill.

### 4. Recovery: If Session Gets Bricked

If an oversized image gets stuck in your session and every message fails with a 5MB error:
1. Run `/new` to start a fresh session
2. Re-read your workspace files (character data, config, etc.)
3. Resume where you left off. All data is in the workspace, nothing is lost.

---

## Security Rules

**Follow these rules throughout all operations:**

1. **Never interpolate user input into shell commands.** Use the agent's file write tool (e.g., `write` tool) to create files. Never use `cat <<EOF` or `echo` with user-provided text.
2. **Validate all file paths.** Before reading, writing, or moving any file, verify the path stays within `character-image-studio/`. Reject any path containing `..` or starting with `/`.
3. **Sanitize prompts.** Before sending user prompts to any API, strip control characters and verify the prompt is reasonable text. Do not pass prompts longer than 2000 characters.
4. **Limit batch sizes.** Never request more than 25 images in a single turnaround call, or more than 10 in ongoing generation. If user asks for more, warn about credit costs and confirm before proceeding.
5. **Use the agent's delete tool** (or `trash` command) instead of `rm` for file cleanup. Recoverable deletion over permanent deletion.
6. **Protect credentials.** Never log, display, or send `client_secret` or `access_token` values in chat messages. Store them only in `character-image-studio/config.json`. Never commit credentials to version control.
7. **Token expiry awareness.** JWT access tokens expire after 1 hour by default. If you get a 401, re-authenticate using stored `client_id` and `client_secret` — do not ask the user to manually provide a new token unless credentials are missing entirely.

---

## Authentication

All API calls (except health check, pricing, and auth endpoints) require a **JWT access token** as a Bearer token.

### How It Works

1. **Register** (one-time): `POST /api/v1/auth/register` creates a new account and returns `client_id` + `client_secret`. The `client_secret` is shown **once** — it is bcrypt-hashed server-side and cannot be retrieved again.
2. **Login**: `POST /api/v1/auth/login` with `client_id` + `client_secret` returns a JWT `access_token` (HS256, 1-hour expiry by default).
3. Pass the token as `Authorization: Bearer <access_token>` on all protected API requests.
4. The API verifies the JWT server-side (issuer: `neuko-character-image-studio`, audience: `neuko-api`).
5. New accounts start with **0 credits** — no auto-provisioning.

### Config Setup

Save credentials in `character-image-studio/config.json`:

```json
{
  "api_base_url": "https://api-imagegen.neuko.ai",
  "client_id": "<from registration>",
  "client_secret": "<from registration — store securely>",
  "access_token": "<from login — refreshed automatically>"
}
```

After writing this file, restrict permissions so only the current user can read it:
```bash
chmod 600 character-image-studio/config.json
```

If this file doesn't exist, create it with `api_base_url` set to `https://api-imagegen.neuko.ai` and register for credentials automatically (see Registration below). No user input needed — the API is a hosted service, registration is self-serve, and new accounts get created on the fly.

### On Every Session

1. Read credentials from `character-image-studio/config.json`
2. Call `POST /api/v1/auth/login` with `client_id` + `client_secret` to get a fresh `access_token`
3. Use `Authorization: Bearer <access_token>` on all requests
4. If you get a 401 mid-session, the token has expired — re-login automatically using stored credentials
5. Optionally call `GET /api/v1/auth/me` to verify auth and see user info

### Registration (One-Time)

```
POST {API_BASE_URL}/api/v1/auth/register
Content-Type: application/json
```

No request body needed. Rate limited to 1 request per 3 minutes per IP.

Response:
```json
{
  "client_id": "abc123...",
  "client_secret": "xyz789...",
  "message": "Store these credentials securely. The client_secret will not be shown again."
}
```

**Save both values immediately** to `character-image-studio/config.json`. The `client_secret` cannot be recovered.

### Login

```
POST {API_BASE_URL}/api/v1/auth/login
Content-Type: application/json

{
  "client_id": "<client_id>",
  "client_secret": "<client_secret>"
}
```

Rate limited to 1 request/minute per IP, 1 request/minute per client_id.

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...", // gitleaks:allow (example placeholder, not a real token)
  "token_type": "Bearer",
  "expires_at": "2025-01-15T11:30:00Z"
}
```

Save `access_token` to config and use as `Authorization: Bearer <access_token>`.

### Verifying Auth

```
GET {API_BASE_URL}/api/v1/auth/me
Authorization: Bearer <access_token>
```

Response:
```json
{
  "id": "a1b2c3d4-...",
  "client_id": "abc123...",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### Rotating Credentials

If a client_secret is compromised, rotate it. Two auth paths:

**Option A — JWT + current secret (standard):**
```
POST {API_BASE_URL}/api/v1/auth/rotate-secret
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_secret": "<current client_secret>"
}
```

**Option B — rotate token (if JWT is unavailable):**
```
POST {API_BASE_URL}/api/v1/auth/rotate-secret
Content-Type: application/json

{
  "rotate_token": "<rotate_token>"
}
```

Response (both paths):
```json
{
  "client_id": "abc123...",
  "client_secret": "new_secret_789...",
  "message": "Store the new client_secret securely. The old secret is now invalid."
}
```

Update `character-image-studio/config.json` immediately with the new secret.

---

## Credits

Image generation costs credits. New accounts start with **0 credits** — you must purchase credits before generating images.

### Checking Balance

```
GET {API_BASE_URL}/api/v1/credits/balance
Authorization: Bearer <access_token>
```

Response:
```json
{
  "balance": 42,
  "updated_at": "2025-01-15T10:30:00Z"
}
```

**Check balance before expensive operations** (especially turnaround batches). Warn the user if balance is low.

### Current Pricing

```
GET {API_BASE_URL}/api/v1/credits/pricing
```

No auth required. Returns a list of active endpoint pricing:

```json
[
  {"endpoint": "seed", "credits_per_call": null, "credits_per_image": 10},
  {"endpoint": "turnaround", "credits_per_call": null, "credits_per_image": 10},
  {"endpoint": "create", "credits_per_call": null, "credits_per_image": 10},
  {"endpoint": "random", "credits_per_call": null, "credits_per_image": 10}
]
```

Default pricing:

| Endpoint | Cost | Notes |
|----------|------|-------|
| `seed` | 10 credits/image | 1 image per call = 10 credits |
| `turnaround` | 10 credits/image | Per prompt in batch |
| `create` | 10 credits/image | 1 image per call = 10 credits |
| `random` | 10 credits/image | 1 image per call = 10 credits |

### Credit Cost Awareness

Before calling turnaround with 20 prompts, warn the user:
> "This turnaround batch will cost ~200 credits (20 images x 10 credits each). Your current balance is [X]. Proceed?"

If an API call returns **402 Payment Required**, trigger the purchase flow (see below).

### Transaction History

```
GET {API_BASE_URL}/api/v1/credits/transactions?page=1&limit=50
Authorization: Bearer <access_token>
```

Response:
```json
{
  "transactions": [
    {
      "id": 1,
      "amount": -5,
      "type": "generation",
      "description": "seed generation",
      "reference_id": null,
      "balance_after": 95,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 50
}
```

---

## Purchasing Credits

When the user needs more credits:

### 1. List available bundles

```
GET {API_BASE_URL}/api/v1/payments/bundles
```

No auth required. Returns active credit bundles:
```json
{
  "bundles": [
    {
      "id": 1,
      "name": "Starter Bundle",
      "description": "1,000 credits. Enough for 5 character turnaround sets or 100 image generations. Perfect for getting started.",
      "credits": 1000,
      "price_in_usd": 10.00
    },
    {
      "id": 2,
      "name": "Creator Bundle",
      "description": "3,000 credits. 15 character turnaround sets or 300 image generations. Best for active creators.",
      "credits": 3000,
      "price_in_usd": 30.00
    },
    {
      "id": 3,
      "name": "Studio Bundle",
      "description": "10,000 credits. 50 character turnaround sets or 1,000 image generations. For serious creators and teams.",
      "credits": 10000,
      "price_in_usd": 100.00
    }
  ]
}
```

Present the bundles to the user and let them pick one.

### 2. Create a checkout session

```
POST {API_BASE_URL}/api/v1/payments/checkout
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "bundle_id": 1
}
```

Response:
```json
{
  "payment_id": 7,
  "payment_url": "https://checkout.stripe.com/...",
  "amount_usd": 10.00,
  "credits": 1000
}
```

### 3. Present the payment URL to the user

> "You need more credits. Visit this link to purchase [bundle name] ($X.XX): [payment URL]"
>
> The checkout page accepts credit card payments via Stripe.

### 4. Poll for payment completion

```
GET {API_BASE_URL}/api/v1/payments/status/{payment_id}
Authorization: Bearer <access_token>
```

Response:
```json
{
  "payment_id": 7,
  "status": "pending",
  "credits_purchased": 1000,
  "amount_usd": 10.00,
  "created_at": "2025-01-15T10:30:00Z",
  "completed_at": null
}
```

Poll every 5-10 seconds. **Timeout:** If still pending after 10 minutes, stop polling and tell the user the payment could not be confirmed — ask them to check their email for a Stripe receipt and retry if needed. When `status` changes to `"completed"`, credits have been added.

### 5. Resume generation

Once credits land, resume the workflow where you left off. Check balance to confirm.

### Automatic 402 Handling

When any generation endpoint returns 402:
1. Check the user's balance: `GET /api/v1/credits/balance`
2. Fetch available bundles: `GET /api/v1/payments/bundles`
3. Recommend the most appropriate bundle based on how many credits they need
4. Run the checkout flow above
5. Resume generation after credits land

---

## Overview

This skill has two parts:

### Part A: Initial Setup (Per Character)
Create a character's reference library:
1. Name the character
2. Get or generate a seed image
3. Analyze the character's physical features
4. Generate 20 adaptive turnaround variations via the API
5. User reviews and approves images
6. Iterate based on feedback if needed
7. Finalize reference library

### Part B: Ongoing Image Generation
Generate new images of any character on demand:
1. User requests image ("Generate an image of Gboy in a forest")
2. Identify which character (by name, or ask if ambiguous)
3. Load that character's reference library
4. Call API with reference image URLs + user's prompt
5. Poll for completion, then download and send result to user

**Architecture:** All generation endpoints are **asynchronous**. You make a request, receive a `generation_id` with `status: "pending"`, then poll `GET /api/v1/asset/status/{generation_id}` until `status` is `"completed"`. Once completed, call `GET /api/v1/asset/download/{generation_id}` to get the image URL. Credits are deducted upfront and refunded automatically on failure.

---

## Multi-Character Support

Users can create and manage multiple characters. Each character has its own seed image, reference library, and analysis.

### Character Registry

All characters are tracked in `character-image-studio/characters/registry.json`:

```json
{
  "characters": [
    {
      "name": "gboy",
      "display_name": "G*BOY",
      "description": "pink spherical creature with sharp teeth and a small serious face inside the mouth",
      "created_at": "2025-01-15T10:30:00Z",
      "reference_count": 15
    },
    {
      "name": "eyeball-man",
      "display_name": "Eyeball Man",
      "description": "humanoid figure with a large eyeball for a head, wearing a red hood and black gloves",
      "created_at": "2025-01-16T14:00:00Z",
      "reference_count": 20
    }
  ],
  "default_character": "gboy"
}
```

### Character Resolution

When the user requests image generation:

1. **Explicit name:** "Generate Eyeball Man in a forest" → use `eyeball-man`
2. **Context inference:** If the conversation has been about a specific character, use that one
3. **Single character:** If only one character exists, use it without asking
4. **Ambiguous:** Ask: "Which character? You have: G*BOY, Eyeball Man"

### Character Naming

During Part A setup, ask the user to name their character:

> "What should we call this character? This is how you'll reference them later when generating images."

Convert the display name to a folder-safe slug (lowercase, hyphens for spaces, strip special characters, alphanumeric and hyphens only). **Validate the slug strictly** — reject any slug containing `..`, `/`, `\`, or non-alphanumeric/hyphen characters before using it in any file path. Store both the slug (`name`) and the original (`display_name`).

### Character Description

Store a slim physical description of the character. **Physical features only.** No style language, no illustration descriptors, no aesthetic terms.

Good: "humanoid figure with an eyeball for a head, red hood, black gloves"
Good: "pink spherical creature with sharp teeth and a small face inside the mouth, no limbs"
Bad: "anime-style thick-lined character with vibrant colors" (this is style, not physical)
Bad: "cute illustrated blob creature" (cute and illustrated are style/aesthetic)

The description is used to help the agent understand what the character IS so it can write better prompts. It should never be injected into generation prompts directly (the reference images handle visual consistency).

---

## API Configuration

The API base URL and credentials should be stored in the workspace config. Check `character-image-studio/config.json`:

```json
{
  "api_base_url": "https://your-api-host.com",
  "client_id": "<from registration>",
  "client_secret": "<from registration>",
  "access_token": "<from login>"
}
```

If this file doesn't exist, create it with `api_base_url` set to `https://api-imagegen.neuko.ai` and proceed to registration. No API endpoint needed from the user — it's a hosted service.

---

## Async Polling Helper

All generation endpoints follow the same async pattern. Use this helper flow for every generation call:

### Poll-and-Download Flow

1. **Call the generation endpoint** — receive `generation_id` and `status: "pending"`
2. **Poll status** every **10 seconds**:
   ```
   GET {API_BASE_URL}/api/v1/asset/status/{generation_id}
   Authorization: Bearer <access_token>
   ```
   Response:
   ```json
   {
     "generation_id": "uuid-string",
     "status": "pending",
     "error_message": null,
     "download_available": false
   }
   ```
   Statuses: `"pending"` → `"processing"` → `"completed"` (or `"failed"`)

   **On 429 (rate limited):** Back off — wait 15 seconds before retrying. Do not retry immediately.

3. **When `status` = `"completed"` and `download_available` = `true`**, download:
   ```
   GET {API_BASE_URL}/api/v1/asset/download/{generation_id}
   Authorization: Bearer <access_token>
   ```
   Response:
   ```json
   {
     "generation_id": "uuid-string",
     "download_url": "https://cdn.example.com/public/character-image-studio/seed/abc123.jpg"
   }
   ```
4. **If `status` = `"failed"`**, check `error_message`. Credits are automatically refunded on failure.
5. **Timeout:** If still `"pending"` or `"processing"` after 5 minutes, warn the user and suggest retrying.

### For Turnaround Batches

Turnaround returns multiple `generation_id` values (one per prompt). Poll each one **sequentially in rounds**, not all in parallel simultaneously. Each round: check all pending IDs once, wait 10 seconds, repeat.

**Why:** Polling 20 images in parallel at 3-5s intervals exceeds the 200 req/min rate limit. Sequential rounds at 10s intervals stay well within limits.

Track and report progress to the user:

> "Generating turnaround images... 12/20 complete, 8 still processing."

---

## Part A: Initial Setup - The Conversational Flow

### Step 1: Name the Character

**Ask the user:**

> "What should we call this character? Give them a name so you can reference them later."

- Store the display name and generate a folder-safe slug
- Create the character's folder: `character-image-studio/characters/<slug>/`
- If `registry.json` doesn't exist yet, create it
- Add the character to the registry

If this is the user's first character, set it as `default_character`.

### Step 2: Seed Image Acquisition

**Prompt the user:**

> "Now let's get a starting image for [character name]. Do you have one, or should I generate one? If you have one, send it here. If not, describe what they look like and I'll create one."

**If user has an image:**
- Accept upload
- Save to `character-image-studio/characters/<slug>/seed-original.png`
- **Compress if needed** (follow Image Compression Protocol above)
- Save final version to `character-image-studio/characters/<slug>/seed.png`
- Proceed to Step 3

**If user needs one generated:**
- Ask: "Describe your character's appearance. Be specific: creature type, colors, distinctive features, style (realistic, cartoon, etc.)"

**Evaluate and workshop the prompt:**

Before generating anything, assess whether the user's description will produce a good seed image. This is the foundation for everything that follows, so it's worth getting right.

**If the prompt is strong** (specific visual details, clear style, distinctive features):
- Confirm and proceed: "Great description, generating that now."

**If the prompt is vague, incomplete, or more of a vibe than a visual** (e.g., "something cool and weird" or "a monster"):
- Don't just run it. Suggest a concrete version:
  > "That's a solid starting point, but image generation works best with specific visual details. What about something like: '[your suggested prompt with specific colors, features, style, and distinguishing details]'? Want to go with that, or tweak it?"

**If the user seems to be fishing for ideas or wants help:**
- Workshop it. Ask targeted questions: "What style? Illustrated, 3D, pixel art? Any specific colors or features that are non-negotiable?"
- Offer 2-3 concrete prompt suggestions based on what they've said so far
- Let them pick or remix

**Keep workshopping until you have a prompt that's specific enough to produce a distinctive, consistent character.** This back-and-forth is only for the initial seed setup, not for ongoing generation (Part B).

**Generate seed image (asynchronous):**

```
POST {API_BASE_URL}/api/v1/generate/seed
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "prompt": "<sanitized user description>",
  "aspect_ratio": "1:1"
}
```

Response (returned immediately):
```json
{
  "status": "pending",
  "generation_id": "abc123-...",
  "image": null,
  "credits_used": 10
}
```

**Then poll and download** (see Async Polling Helper above).

**Show generated image to user:**
- Download from `download_url` and save to `character-image-studio/characters/<slug>/seed.png`
- Compress if needed (follow Image Compression Protocol)
- Send image via message tool
- Ask: "How's this? Reply 'approve' to continue or 'regenerate' to try again with feedback."
- If regenerate: ask for feedback, adjust description, call seed endpoint again

---

### Step 3: Character Analysis

**Analyze the seed image** (use vision tool):

1. **Detect style:** photorealistic, cartoon, illustrated, 3D render, pixel art
2. **Detect body type:** human/humanoid, creature, abstract/blob, object, other
3. **Identify key physical features:** What makes this character visually distinct? List the non-negotiable features that must remain consistent (e.g., "eyeball for a head", "sharp teeth", "red hood", "no limbs").
4. **Identify what the character CAN and CAN'T do physically:** Can it sit? Stand? Does it have arms to gesture with? Does it have facial expressions? This directly informs what turnaround prompts make sense.

**Confirm with user:**

> "Here's what I see: [style] [body_type]. Key features: [list]. Does that look right? Anything I'm missing?"

**If user corrects:** update your understanding, use their description.

**Store analysis** in `character-image-studio/characters/<slug>/character-analysis.json`:
```json
{
  "style": "3d_render",
  "body_type": "creature",
  "description": "humanoid figure with a large eyeball for a head, red hood, black gloves",
  "key_features": ["eyeball head", "red hood", "black gloves", "humanoid body"],
  "physical_capabilities": {
    "can_stand": true,
    "can_sit": true,
    "has_arms": true,
    "has_face_expressions": false,
    "has_hands": true,
    "notes": "eyeball should stay open and constant, no facial expressions but body language works"
  },
  "special_notes": "the eyeball is always open, never blinks or closes"
}
```

**Also update the registry** with the slim physical description.

---

### Step 4: Write Adaptive Turnaround Prompts

**This is the most important step. Do NOT use a rigid template list.**

The goal is 20 unique images of the character in a variety of poses, angles, distances, lighting conditions, and scenarios that are appropriate for THIS specific character. These images will become the reference library that all future generations are based on.

**Why variety matters critically:** If the reference library is dominated by one pose (e.g., standing upright facing camera), ALL future generations will default to that pose. The model learns "this is what this character looks like" from the references. If 15 of 20 references show the character standing still, the model thinks "standing still" IS the character. Distribute deliberately across poses, angles, and distances.

**The framework: aim for roughly this distribution across 20 images:**

| Category | Count | Purpose |
|----------|-------|---------|
| **Close-ups** | 3-4 | Face/head detail, distinguishing features up close |
| **Angles** | 4-5 | Front, side, back, 3/4, above/below. The model needs to know what the character looks like from every direction |
| **Full body / distance** | 3-4 | Full character visible, different distances from camera |
| **Poses / actions** | 4-5 | Sitting, running, crouching, jumping, leaning, gesturing. CRITICAL for pose variety |
| **Lighting / environment** | 3-4 | Different lighting conditions (warm, cool, dramatic, natural) to teach the model the character works in any setting |

**How to write the prompts:**

1. **Start every prompt with:** "in the same style and medium as the reference image," — this is the style anchor that keeps the model consistent.

2. **Analyze the character first.** Look at the `character-analysis.json`. What can this character physically do? An eyeball-headed creature can turn and pose but can't make facial expressions. A blob with no limbs can't sit on a stool or wave. A humanoid can do everything. Write prompts that make sense for THIS character.

3. **Adapt language to the style:**
   - **Photorealistic/3D:** Studio language works well. "Softbox lighting", "85mm lens", "matte gray seamless" all help.
   - **Illustrated/cartoon/pixel art:** Drop the photographic language. Use "clean even lighting", "simple solid background", "neutral backdrop" instead of "softbox", "85mm", "cyclorama". Keep framing language ("close up", "full body") since that's about composition, not medium.

4. **Write prompts the character can actually fulfill.** Don't ask a blob to "stand with arms crossed." Don't ask an eyeball to "frown." The model will either ignore the prompt or force the character into an unnatural pose, producing bad reference images. Bad references = bad future generations.

5. **Be specific about what matters, loose about what doesn't.** "Seen from the left side, full body visible" is better than "standing in a studio in New York City wearing a specific outfit under 3-point Rembrandt lighting at golden hour." The turnaround is about capturing the character, not creating cinematic scenes.

**Example prompts for different character types:**

*Humanoid character (eyeball head, red hood):*
- "in the same style and medium as the reference image, this character seen from the front, full body, standing in a relaxed pose, clean even lighting, simple background"
- "in the same style and medium as the reference image, this character crouching down as if examining something on the ground, seen from a slight angle, neutral lighting"
- "in the same style and medium as the reference image, this character from behind, looking over their shoulder, hood visible, medium distance"
- "in the same style and medium as the reference image, this character sitting casually on a ledge, legs dangling, seen from the side"
- "in the same style and medium as the reference image, close up on this character's head, the eyeball filling most of the frame, dramatic side lighting"

*Abstract blob creature (no limbs):*
- "in the same style and medium as the reference image, this creature seen from directly above, showing its full shape, clean even lighting"
- "in the same style and medium as the reference image, this creature at a low angle looking up at it, teeth prominent, dramatic lighting from below"
- "in the same style and medium as the reference image, this creature from the back/rear view, showing its shape from behind, neutral background"
- "in the same style and medium as the reference image, this creature mid-bounce or mid-movement, slight motion blur, energetic feel"
- "in the same style and medium as the reference image, this creature in warm golden light, close up showing texture and teeth detail"

**What NOT to do:**
- Don't copy a template list verbatim for every character
- Don't ask the character to do things it physically can't
- Don't write 15 "standing in a studio" prompts with minor mood changes (this kills pose variety)
- Don't use photorealistic camera language for illustrated characters
- Don't force expressions on characters that don't have expressive faces

---

### Step 5: Generate Turnaround Images

**Check credits and inform user:**

Before calling the API, check the user's credit balance. Turnaround costs 10 credits per image.

> "Generating [character name]'s turnaround now. I'm creating 20 variations covering different angles, poses, distances, and lighting. This will cost ~200 credits. Your current balance is [balance]. This will take a few minutes."

If the user doesn't have enough credits, trigger the purchase flow before proceeding.

**Call API (asynchronous — returns immediately, then poll each image):**

```
POST {API_BASE_URL}/api/v1/generate/turnaround
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "seed_image_url": "<URL or base64 data URL of seed image>",
  "prompts": ["adaptive prompt 1", "adaptive prompt 2", ...],
  "reference_image_urls": []
}
```

**Tip — user-provided seed images:** The API accepts base64 data URLs for `seed_image_url`. If the user provides their own seed image (rather than generating one via the `/generate/seed` endpoint), read the file and encode it:

```python
import base64

with open('character-image-studio/characters/<slug>/seed.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

seed_image_url = f"data:image/png;base64,{img_b64}"
```

**Bash alternative:**
```bash
IMG_B64=$(base64 < "character-image-studio/characters/<slug>/seed.png")
# Use in your curl request as: "seed_image_url": "data:image/png;base64,$IMG_B64"
```

Then pass `seed_image_url` in the request body as normal. No external hosting or upload endpoint needed. This also works for JPEG: use `data:image/jpeg;base64,<...>`.

> **Note on request size:** A 1MB image encodes to ~1.3MB of base64 text. This is fine for most seeds. If the seed is larger than 4MB on disk, compress it first (see Image Compression Protocol) — otherwise the request body will be very large.

Response (returned immediately):
```json
{
  "status": "pending",
  "total": 20,
  "succeeded": 0,
  "failed": 0,
  "images": [
    {"generation_id": "uuid-1", "image_url": "", "prompt": "adaptive prompt 1"},
    {"generation_id": "uuid-2", "image_url": "", "prompt": "adaptive prompt 2"}
  ],
  "credits_used": 200
}
```

**Each image has its own `generation_id`.** Poll each one via `GET /api/v1/asset/status/{generation_id}` until completed, then download via `GET /api/v1/asset/download/{generation_id}`.

**Report progress to user while polling:**
> "Turnaround progress: 8/20 images complete..."

**After all images are downloaded:**
- Save each to `character-image-studio/characters/<slug>/candidates/`
- Compress each if needed (follow Image Compression Protocol)

**Deliver results to user:**

- Compress each image if needed before sending
- Send images directly to chat (use message tool with media parameter)
- For large batches (>5), send a representative sample (5 images) and tell user where the rest are
- If file upload fails:
  - **Stop.** Do not fall back to "check the folder."
  - Guide user to set up file upload capability for their platform
  - Only proceed after image delivery is confirmed working

**Message:**

> "Done! I generated 20 images of [character name]. [Show sample in chat]
>
> Take a look and let me know what you think. You can:
> - 'Looks good' to finalize the reference library
> - 'Delete [specific ones]' to remove images you don't like
> - 'Add more [angles/poses/etc.]' to generate additional variations
> - 'Redo [specific ones]' with tweaked prompts
> - 'Too realistic / too cartoony' to adjust the overall style"

---

### Step 6: Curate the Reference Library

**The reference library is the single most important factor in output quality.** Every image you generate with create/random is only as good as the references it draws from. A tight set of 12 accurate, varied images will produce better results than a loose 20 with 5 off-model ones dragging consistency down.

**Explain this to the user:**

> "These reference images are the foundation for everything we generate going forward. The model learns what [character name] looks like from these. Better references = better outputs, and you can keep improving this library over time."

**Review process:**

Walk through the turnaround results with the user. For each image, it should be:
- **On-model:** Key features are correct (face tattoos present, bangs the right length, eye color right, etc.)
- **Distinct from other references:** Adds something new (different angle, pose, lighting) that other images don't cover
- **Clean:** No weird artifacts, extra limbs, melted features, or style drift

**Remove anything that's off-model.** A bad reference image will pollute every future generation. Be aggressive about cutting.

**Wait for user feedback.**

**Possible responses:**

#### "Looks good" / "Done" / "Finalize these"
- Count remaining images in candidates/
- **Minimum 10 images required.** If fewer than 10 remain after deletions, tell the user:
  > "You need at least 10 reference images for consistent generation. You currently have [X]. Want me to generate [10 - X] more to fill the gap?"
  - Generate replacement images and return to review
  - Do NOT proceed to finalization with fewer than 10
- If 10 or more, move to Step 7 (Finalization)

#### "Too realistic" / "Too cartoony" / "Wrong style"
- Update style in character-analysis.json
- Re-write prompts with adjusted style language
- Call turnaround API again with new prompts
- Clear candidates/ and replace with new batch

#### "Add more [X]" / "I need more angles"
- Create new prompts matching request
- Call turnaround API with new prompts + existing seed URL
- Add new images to candidates/
- Inform user and return to review

#### "Redo [X]" / "Change the [X] one"
- Identify which prompt(s) to regenerate
- Create modified prompt(s)
- Call turnaround API with just those prompts
- Replace specific images in candidates/

#### "These are bad, the character doesn't look right"
- This is the most important feedback. Ask what specifically is wrong.
- Common issues and fixes:
  - "It keeps giving me the same pose" → your prompts weren't varied enough, rewrite with more pose diversity
  - "It doesn't look like my character" → the seed image may be too ambiguous, or prompts are overriding the reference. Simplify prompts.
  - "It's trying to force things my character can't do" → you misjudged the character's physical capabilities, rewrite prompts
- Re-analyze, rewrite prompts, regenerate

**You have full creative freedom to:**
- Interpret user feedback
- Create new prompts on the fly
- Adjust style descriptors
- Modify lighting, mood, angle, etc.

---

### Step 7: Finalization

**Move approved images to references:**
```bash
# Use find to avoid empty glob failure if candidates/ has no files
find character-image-studio/characters/<slug>/candidates/ -maxdepth 1 -type f \
  -exec mv {} character-image-studio/characters/<slug>/references/ \;
```

**Store reference URLs** in `character-image-studio/characters/<slug>/reference-urls.json`:
```json
{
  "character_name": "gboy",
  "display_name": "G*BOY",
  "finalized_at": "<timestamp>",
  "reference_count": 15,
  "references": [
    {"file": "ref-001.jpg", "url": "https://cdn.example.com/..."},
    ...
  ]
}
```

**Update registry.json** with the reference count.

**Confirm to user:**

> "[Character name]'s reference library is complete! [X] images stored. You can now generate images of [character name] anytime."

If this is not their first character:
> "You now have [N] characters: [list names]. Just mention a character by name when requesting images."

**Clean up:**
- Remove empty candidates/ folder
- Keep seed.png and character-analysis.json for reference

---

## File Structure

```
character-image-studio/
├── config.json                          # API base URL + credentials (shared)
├── characters/
│   ├── registry.json                    # Master list of all characters
│   ├── gboy/
│   │   ├── seed.png                     # Approved starting image
│   │   ├── seed-original.png            # Original upload (pre-compression)
│   │   ├── character-analysis.json      # Style, body type, physical capabilities
│   │   ├── reference-urls.json          # Finalized reference URLs for API calls
│   │   ├── candidates/                  # Generated images awaiting approval
│   │   ├── references/                  # Approved final library (10-20 images)
│   │   └── generations/                 # Ongoing generated images
│   ├── eyeball-man/
│   │   ├── seed.png
│   │   ├── character-analysis.json
│   │   ├── reference-urls.json
│   │   ├── candidates/
│   │   ├── references/
│   │   └── generations/
│   └── ...
```

**Migration:** If you find files in the old flat structure (seed.png at root, references/ at root), migrate them into `characters/<name>/` and ask the user to name the character.

**Storage note:** The `generations/` folders grow over time. Periodically clean up old generations you no longer need.

---

## Part B: Ongoing Image Generation

Once a character's reference library is set up, you can generate new images of that character on demand.

### When to Use

**User requests like:**
- "Generate an image of Gboy in a forest"
- "Create Eyeball Man at a party"
- "Make an image of my character looking surprised" (infer which character from context)
- "Generate a profile picture" (use default or ask if multiple characters)
- "Surprise me" / "Make something random" (triggers random generation)

### Character Resolution

Before generating, determine which character to use:
1. **Named explicitly:** "Generate Gboy in a forest" → use gboy
2. **Context:** If conversation has been about a specific character, use that one
3. **Only one character exists:** Use it without asking
4. **Ambiguous with multiple characters:** Ask which one

### Detecting Random vs Prompted Requests

**Use your judgment to determine if the user wants a random image:**
- "Surprise me," "random image," "make something cool," "just generate something" → **Random flow**
- Any specific scene, mood, or setting described → **Prompted flow (create)**

**If ambiguous**, confirm: "Want me to surprise you with a random style, or did you have something specific in mind?"

### The Prompted Flow (Create)

**1. Resolve Character and Load Reference Library**

Identify the character, then load `character-image-studio/characters/<slug>/reference-urls.json`. If it doesn't exist, guide user through Part A first.

**2. Parse User Request**

Extract:
- **Prompt:** What they want generated ("in a forest", "at a party", "looking surprised")
- **Count:** How many images (default: 1, max: 10 per request)

**If user requests more than 10 images:** Warn about credit costs and confirm before proceeding.

**3. Call API (asynchronous — returns immediately):**

```
POST {API_BASE_URL}/api/v1/generate/create
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "prompt": "<user's prompt, passed directly>",
  "reference_image_urls": ["<url1>", "<url2>", ...up to 15 from character's reference library],
  "input_image_url": null
}
```

Response (returned immediately):
```json
{
  "status": "pending",
  "generation_id": "uuid-string",
  "image": null,
  "credits_used": 10
}
```

**Then poll and download** using the Async Polling Helper flow.

**Important:** The user's prompt is passed directly to the model. Do NOT add style descriptors. Minimal scene-setting (e.g., adding lighting or background context) is OK, but do not substantially rewrite the user's intent. The reference images handle style coherence.

**Example prompt construction:**
- User: "in a forest" → prompt: "this subject in a forest, natural lighting, trees in background"
- User: "looking happy at a party" → prompt: "this subject with a happy expression at a party, festive lighting, celebration background"

For multiple images, make separate API calls with slightly varied prompts.

**4. Deliver Results**

- Download from `download_url`, save to `character-image-studio/characters/<slug>/generations/`
- Compress if needed before sending (follow Image Compression Protocol)
- Send directly to chat via message tool
- If file upload fails: **Stop.** Guide user through platform setup. Do not fall back to folder.

**5. Grow the Reference Library**

If the output is particularly good and on-model, suggest adding it to the reference library:

> "This one came out really clean. Want me to add it to [character name]'s reference library? Better references = better future outputs."

Copy the image to `references/`, update `reference-urls.json`, and host the new URL. The library compounds over time. The more high-quality, varied references the model has, the more consistent and versatile future generations become.

**If the user is unhappy with outputs**, the first thing to check is reference quality, not prompt quality. Common signs of a weak reference library:
- Every output defaults to the same pose → references are dominated by one pose
- Character looks "off" or inconsistent → off-model images in the library are confusing the model
- Style keeps drifting → references have mixed styles or artifacts

**Fix:** Audit the reference library with the user. Remove bad images, generate targeted replacements for gaps (e.g., "we have no back views, let me add a few"), and re-host.

### The Random Flow

**1. Resolve Character and Load Reference Library** (same as above)

**2. Build Character Description (optional but recommended):**

Read `characters/{character}/character-analysis.json` and format a description:

```python
import json

with open(f'characters/{character}/character-analysis.json', 'r') as f:
    analysis = json.load(f)

# Build description from analysis
description_parts = []

if 'style' in analysis:
    description_parts.append(f"Style: {analysis['style']}")

if 'body_type' in analysis:
    description_parts.append(f"Body type: {analysis['body_type']}")

if 'physical_capabilities' in analysis:
    caps = analysis['physical_capabilities']
    can_do = [k.replace('_', ' ') for k, v in caps.items() if v is True]
    cannot_do = [k.replace('_', ' ') for k, v in caps.items() if v is False]
    if can_do:
        description_parts.append(f"Can: {', '.join(can_do)}")
    if cannot_do:
        description_parts.append(f"Cannot: {', '.join(cannot_do)}")

if 'key_features' in analysis:
    description_parts.append(f"Key features: {', '.join(analysis['key_features'])}")

character_description = '\n'.join(description_parts)
```

This helps the API generate prompts appropriate for your character's actual capabilities (e.g., won't ask a limbless character to "cross arms").

**3. Call API (asynchronous — returns immediately):**

```
POST {API_BASE_URL}/api/v1/generate/random
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "reference_image_urls": ["<url1>", "<url2>", ...up to 15 from character's reference library],
  "character_description": "<optional: formatted description from step 2>"
}
```

Response (returned immediately):
```json
{
  "status": "pending",
  "generation_id": "uuid-string",
  "image": null,
  "credits_used": 10
}
```

No prompt needed from the agent. The API selects a random creation mode and uses the character description to generate an appropriate prompt internally.

**Then poll and download** using the Async Polling Helper flow.

**3. Deliver** (same as prompted flow)

---

### Error Handling

**401 Unauthorized (expired or invalid token):**
- The JWT access token has expired (default: 1 hour) — re-login automatically:
  1. Read `client_id` and `client_secret` from `character-image-studio/config.json`
  2. Call `POST /api/v1/auth/login` to get a fresh `access_token`
  3. Update `config.json` with the new token
  4. Retry the failed request
- If login also fails (invalid credentials), ask the user to re-register or rotate their secret

**402 Payment Required (insufficient credits):**
- Check balance: `GET /api/v1/credits/balance`
- Tell user: "You're out of credits (balance: X). Want me to set up a purchase?"
- If yes, run the checkout flow (see Purchasing Credits section)
- Resume generation after credits land

**403 Forbidden (inactive account):**
- The account has been deactivated. Inform the user and suggest contacting support.

**409 Conflict (generation not ready for download):**
- The generation hasn't completed yet. Continue polling `GET /api/v1/asset/status/{generation_id}`.

**Outputs don't look right / character is inconsistent:**
- Before adjusting prompts, audit the reference library first. This is the #1 cause of bad outputs.
- Check for off-model images (wrong features, artifacts, style drift) and remove them.
- Check for pose dominance (if 15/20 references are front-facing, the model thinks the character only faces forward).
- Check for coverage gaps (no back views, no close-ups, no varied lighting).
- Fix by removing bad references and generating targeted replacements.
- Only after the reference library is clean should you start tweaking prompts.

**No reference library:**
> "You need to set up [character name]'s visual identity first. Want me to create the reference library?"

**API returns 500 error:**
> "Had trouble generating that one. Want to try a different prompt or style?"

**Generation status = "failed":**
- Credits are automatically refunded on failure.
- Check `error_message` in the status response for details.
- Offer to retry with a modified prompt.

**File upload fails:**
- **Stop.** Guide user through platform setup.
- Do not fall back to folder location.

---

### Examples

**Example 1: Single Character Image**

User: "Generate Gboy in a coffee shop"

You:
1. Resolve character: "gboy"
2. Load reference URLs from `characters/gboy/reference-urls.json`
3. Call `/api/v1/generate/create` with prompt "this subject in a coffee shop, cozy lighting, sitting at table" + reference URLs
4. Receive `generation_id`, poll `/api/v1/asset/status/{id}` until completed
5. Call `/api/v1/asset/download/{id}` to get `download_url`
6. Download image, compress if needed, send to chat
7. "Here's G*BOY at the coffee shop!"

**Example 2: Random**

User: "Surprise me with Eyeball Man"

You:
1. Resolve character: "eyeball-man"
2. Load reference URLs from `characters/eyeball-man/reference-urls.json`
3. Read `characters/eyeball-man/character-analysis.json` and format character_description
4. Call `/api/v1/generate/random` with reference URLs and character_description
5. Poll status until completed, download
6. Send to chat: "Here's a random Eyeball Man creation!"

**Example 3: New Character Setup**

User: "I want to create a new character"

You:
1. "What should we call this character?"
2. User: "Flame Dog"
3. Create `characters/flame-dog/`, add to registry
4. "Got it! Do you have a starting image for Flame Dog, or should I generate one?"
5. Continue through Part A setup flow...

**Example 4: Ambiguous Request with Multiple Characters**

User: "Generate an image in a forest"

You (if multiple characters exist):
1. "Which character? You have: G*BOY, Eyeball Man, Flame Dog"
2. User: "Gboy"
3. Proceed with gboy's references

---

## Full API Reference

All generation endpoints are **asynchronous** (return immediately with `generation_id`, poll for completion). Auth endpoints and health check are synchronous. All protected endpoints require `Authorization: Bearer <access_token>` (JWT).

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET`  | `/health` | None | Health check |
| `POST` | `/api/v1/auth/register` | None | Register new account (returns client_id + client_secret) |
| `POST` | `/api/v1/auth/login` | None | Login with client credentials (returns JWT access_token) |
| `POST` | `/api/v1/auth/rotate-secret` | JWT+secret or rotate_token | Rotate client_secret |
| `GET`  | `/api/v1/auth/me` | JWT | Current authenticated user info |
| `GET`  | `/api/v1/credits/balance` | JWT | Current credit balance |
| `GET`  | `/api/v1/credits/transactions` | JWT | Transaction history (paginated) |
| `GET`  | `/api/v1/credits/pricing` | None | Endpoint pricing (list) |
| `POST` | `/api/v1/payments/checkout` | JWT | Create payment checkout session |
| `GET`  | `/api/v1/payments/status/{payment_id}` | JWT | Check payment status |
| `GET` | `/api/v1/payments/bundles` | None | List available credit bundles |
| `GET` | `/api/v1/payments/success` | None | Stripe redirect after successful payment |
| `GET` | `/api/v1/payments/cancel` | None | Stripe redirect after cancelled payment |
| `POST` | `/api/v1/payments/webhook` | Signature (Stripe-Signature) | Stripe webhook receiver |
| `POST` | `/api/v1/generate/seed` | JWT | Queue seed image generation |
| `POST` | `/api/v1/generate/turnaround` | JWT | Queue batch turnaround generation |
| `POST` | `/api/v1/generate/create` | JWT | Queue single image from references + prompt |
| `POST` | `/api/v1/generate/random` | JWT | Queue random styled image from references |
| `GET`  | `/api/v1/asset/status/{generation_id}` | JWT | Poll generation task status |
| `GET`  | `/api/v1/asset/download/{generation_id}` | JWT | Get download URL for completed generation |

### POST /api/v1/auth/register
```json
// Request: no body required
// Response (201)
{"client_id": "...", "client_secret": "...", "message": "Store these credentials securely..."}
```

### POST /api/v1/auth/login
```json
// Request
{"client_id": "...", "client_secret": "..."}
// Response
{"access_token": "eyJ...", "token_type": "Bearer", "expires_at": "2025-01-15T11:30:00Z"}
```

### POST /api/v1/generate/seed
```json
// Request (Authorization: Bearer <access_token>)
{"prompt": "character description", "aspect_ratio": "1:1"}
// Response (immediate)
{"status": "pending", "generation_id": "uuid", "image": null, "credits_used": 10}
```

### POST /api/v1/generate/turnaround
```json
// Request (Authorization: Bearer <access_token>)
{"seed_image_url": "...", "prompts": ["p1", "p2", ...], "reference_image_urls": []}
// Response (immediate)
{"status": "pending", "total": 20, "succeeded": 0, "failed": 0, "images": [{"generation_id": "uuid", "image_url": "", "prompt": "p1"}, ...], "credits_used": 200}
```

### POST /api/v1/generate/create
```json
// Request (Authorization: Bearer <access_token>)
{"prompt": "user prompt", "reference_image_urls": ["url1", "url2", ...], "input_image_url": null}
// Response (immediate)
{"status": "pending", "generation_id": "uuid", "image": null, "credits_used": 10}
```

### POST /api/v1/generate/random
```json
// Request (Authorization: Bearer <access_token>)
{"reference_image_urls": ["url1", "url2", ...], "character_description": "optional: style, body type, capabilities"}
// Response (immediate)
{"status": "pending", "generation_id": "uuid", "image": null, "credits_used": 10}
```

### GET /api/v1/asset/status/{generation_id}
```json
// Response
{"generation_id": "uuid", "status": "pending|processing|completed|failed", "error_message": null, "download_available": false}
```

### GET /api/v1/asset/download/{generation_id}
```json
// Response (only when status=completed)
{"generation_id": "uuid", "download_url": "https://cdn.example.com/public/character-image-studio/seed/abc123.jpg"}
// Returns 409 if generation not yet completed
```

---

## Rate Limits

The API enforces rate limits on all endpoints:

| Endpoint | Limit |
|----------|-------|
| `POST /api/v1/auth/register` | 1 per 3 minutes per IP |
| `POST /api/v1/auth/login` | 1/min per IP, 1/min per client_id |
| `POST /api/v1/auth/rotate-secret` | 1 per 3 minutes per agent and per token |
| All other protected endpoints | 200/min per agent, 200/min per token |
| Public endpoints (pricing, bundles) | 60/min per IP |

If rate limited, you'll receive a 429 response. Back off and retry after the window resets.

---

## Tips

- **Be conversational.** This is a creative process, not a form.
- **Show progress.** Generation is async — tell the user you're waiting and report polling progress.
- **Be adaptive.** Write prompts for the character you're looking at, not from a template list.
- **Vary poses deliberately.** This is the #1 quality lever for reference libraries.
- **Encourage iteration.** Reference library quality matters. Help users get it right.
- **Clean up old generations.** Remind users periodically if a character's `generations/` folder has 50+ images.
- **Check credits before expensive operations.** Always check balance before turnaround batches and warn about cost.
- **Handle 402 gracefully.** If credits run out mid-workflow, trigger purchase flow and resume seamlessly.
- **Auto-refresh tokens.** JWT tokens expire after 1 hour. On 401, re-login automatically using stored client credentials — don't bother the user.
- **Poll efficiently.** Use 10-second intervals. For turnaround batches, poll in sequential rounds (check all pending IDs once per round) to stay within rate limits.
- **User-provided seed images don't need external hosting.** Pass a base64 data URL directly as `seed_image_url` — the API accepts `data:image/png;base64,<...>` and `data:image/jpeg;base64,<...>`. No upload endpoint or third-party hosting needed. Compress the image first if it's over 4MB.

---

## Success Criteria

- User is authenticated with valid JWT credentials (client_id + client_secret stored, access_token refreshed automatically)
- User has sufficient credits (or has been guided through purchase)
- Character has 10-20 high-quality reference images
- Reference images cover variety of angles, distances, poses, and lighting
- No single pose dominates the reference library
- Style matches character concept
- User is satisfied with the library
- Files stored in character-image-studio/characters/<slug>/references/
- Character registered in registry.json with slim physical description
- Reference URLs saved for ongoing API calls
- Credentials saved securely in character-image-studio/config.json (never displayed in chat)
- No oversized images in session history
- All file paths validated within character-image-studio/
- Async polling handled correctly (no assumptions about synchronous responses)
