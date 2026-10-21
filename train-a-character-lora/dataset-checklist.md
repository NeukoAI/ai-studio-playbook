# Dataset checklist: character LoRA

Sources: Replicate's fast trainer page and the ostris trainer README, read 2026-10-20. Lines about our pipeline come from NEUKO's code.

## Count

- [ ] 10 to 20 images. The fast trainer page says 10 to 20; its schema says a minimum of 10. The ostris README says 12 to 18.
- [ ] Our user pipeline allowed up to 200 images. Replicate's guidance is far lower, so start at 10 to 20 and add only images that show something new.

## Size and format

- [ ] Around 1024x1024. Very large images get scaled down to about 1024. To shrink a folder in place on macOS: `sips -Z 1024 *.png`.
- [ ] JPEG or PNG.
- [ ] Sharp, not upscaled from thumbnails.

## Angles (one character, many views)

- [ ] Front, standing, full body (2 to 3)
- [ ] Three-quarter left and right (2 to 4)
- [ ] Side profile (1 to 2)
- [ ] Back (1)
- [ ] Close-up of the face or head (2 to 3)
- [ ] The signature expression (for G\*BOY, the jagged grin) (2)
- [ ] Two or three in different settings and lighting, so the LoRA learns the character, not the background

A turnaround sheet is a good source: cut each view into its own image.

## Captions

- [ ] One `.txt` per image, same file name (`img_01.png` and `img_01.txt`).
- [ ] Every caption starts with the trigger word.
- [ ] Caption what changes (view, pose, expression, setting, light). See `caption-template.txt`.
- [ ] Or leave captions out and let the trainer autocaption. Check a few by hand if you do.

## Leave out

- [ ] Other characters in frame.
- [ ] Text, logos, watermarks, UI, speech bubbles.
- [ ] Outfit or age variants. Replicate's page warns against different haircuts or ages for character LoRAs.
- [ ] Many shots of hands framing the face. Replicate found this led to more hand hallucinations.
- [ ] Near-duplicates. Ten frames from one clip teach one pose.
- [ ] Off-model fan art or early drafts.
- [ ] Heavy crops that hide the outfit.

## Before you zip

- [ ] Images and their `.txt` files sit side by side in the zip (we keep them at the root).
- [ ] Open five random images next to each other. If you can't tell they are the same character, neither can the trainer.
