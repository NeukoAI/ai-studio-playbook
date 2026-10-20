# Archive

Skills we no longer maintain. They stay here for reference.

## character-image-studio

This skill drives the NEUKO Character Image Studio API (`api-imagegen.neuko.ai`). Registration is self-serve, but new accounts start with 0 credits. On 2026-10-20 the credit bundles endpoint (`/api/v1/payments/bundles`) timed out on three tries, so a new user could not buy credits or make an image. The skill also assumes an OpenClaw gateway.

To keep a character consistent today, use [`train-a-character-lora/`](../train-a-character-lora/). It runs on your own Replicate account and covers both the LoRA route and the reference-image route.
