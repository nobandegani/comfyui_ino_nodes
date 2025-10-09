import hashlib
import random

#---------------------------------InoRandomCharacterPrompt
class InoRandomCharacterPrompt:
    """
        Random Character Prompt
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),

                "main": ("STRING", {
                    "multiline": True,
                    "label": "Main prompt",
                    "default": "blonde hair, oval face, Caucasian, fair skin, 20-30 years old, female"
                }),

                "finetune": ("STRING", {
                    "multiline": True,
                    "label": "Finetune prompt",
                    "default": "pretty, naked, Hair Elegant braided top knot bun, consistent facial features across all 4 frames"
                }),

                "lighting": ("STRING", {
                    "multiline": True,
                    "default": "The lighting is soft and matte, with no gloss or facial shine. The light is evenly diffused and balanced to avoid specular highlights or reflective hotspots on the skin. The face appears naturally lit, with smooth shadows and a non-reflective finish."
                }),

                "camera": ("STRING", {
                    "multiline": True,
                    "default": "Captured with a high-quality DSLR camera using a wide aperture lens, producing a shallow depth of field and a sharp, detailed image. The result is a super realistic portrait with professional photography quality and natural skin tones."
                }),

                "background": ("STRING", {
                    "multiline": True,
                    "default": "The background is plain white, clean and seamless, without texture or distractions."
                }),

                "random_face_shape": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eyebrow_shapes": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eyebrow_thickness": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eye_colors": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eye_shapes": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eyelashes": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eyelid_types": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_nose_shapes": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_nose_sizes": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_lip_shapes": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_lip_sizes": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_lip_fullness": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_cheek_bones": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_jawline": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_chin": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_makeup_style": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_beauty_marks": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", )
    RETURN_NAMES = ("Prompt", "Seed", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    def get_index(self, seed, offset, length):
        return (seed + offset) % length

    def function(
        self,
        seed,
        main, finetune, lighting, camera, background,
        random_face_shape,
        random_eyebrow_shapes, random_eyebrow_thickness,
        random_eye_colors, random_eye_shapes,
        random_eyelashes, random_eyelid_types,
        random_nose_shapes, random_nose_sizes,
        random_lip_shapes, random_lip_sizes, random_lip_fullness,
        random_cheek_bones, random_jawline, random_chin,
        random_makeup_style, random_beauty_marks
    ):

        if seed == 0:
            seed_number = random.seed(seed)
            use_random = True
        else:
            use_random = False

        parts = [main, finetune]

        def pick(options, offset):
            if use_random:
                return random.choice(options)
            else:
                return options[self.get_index(seed, offset, len(options))]

        if random_face_shape:
            face_shapes = [
                "oval",
                "heart-shaped",
                "diamond",
                "square",
                "round",
                "long",
                "soft triangle",
                "inverted triangle",
                "pear-shaped",
                "slim angular",
                "broad forehead with narrow chin shape",
                "delicate V-shaped",
                "contoured oval with high cheekbones"
            ]
            choice=pick(face_shapes, 10)
            parts.append(choice + " face shape")

        if random_eyebrow_shapes:
            eyebrow_shapes = [
                "soft arched",
                "high arched",
                "straight",
                "rounded",
                "curved",
                "slightly angled",
                "feathered arch",
                "flat and wide",
                "slim and lifted",
                "natural arch"
            ]
            choice=pick(eyebrow_shapes, 10)
            parts.append(choice + " eyebrow shape")

        if random_eyebrow_thickness:
            eyebrow_thickness = [
                "ultra thin",
                "thin",
                "medium thickness",
                "thick",
                "bold and defined",
                "full and natural",
                "fluffy",
                "structured but soft"
            ]
            choice=pick(eyebrow_thickness, 10)
            parts.append(choice + " eyebrow thickness")

        if random_eye_colors:
            eye_colors = [
                "warm hazel with golden flecks",
                "light amber with honey undertones",
                "deep espresso brown",
                "cool gray-blue",
                "forest green with subtle brown rings",
                "emerald green with a vibrant shimmer",
                "soft olive green",
                "icy blue with silver highlights",
                "sky blue with a hint of teal",
                "steel gray with a soft blue tint",
                "light brown with a hint of amber glow",
                "dark brown with reddish undertones",
                "gray-green blend with a soft matte finish",
                "light hazel with a green inner ring",
                "blue-gray with pale speckles",
                "moss green with warm golden centers",
                "cool taupe-gray",
                "greenish hazel with a copper halo",
                "light slate blue with dark limbal ring"
            ]
            choice=pick(eye_colors, 10)
            parts.append(choice + " eye color")

        if random_eye_shapes:
            eye_shapes = [
                "almond-shaped",
                "round",
                "monolid",
                "hooded",
                "upturned",
                "downturned",
                "deep-set",
                "protruding",
                "close-set",
                "wide-set",
                "cat-like",
                "droopy",
                "fox",
                "doe",
                "slanted",
                "tapered",
                "asymmetrical",
                "narrow",
                "large soft",
                "sharp angular"
            ]
            choice=pick(eye_shapes, 10)
            parts.append(choice + " eye shape")

        if random_eyelashes:
            eyelashes = [
                "long and curled",
                "naturally thick",
                "defined and lifted",
                "full and fluttery",
                "soft wispy",
                "voluminous cat-eye",
                "outer corner accent",
                "bold doll-like",
                "delicate lower",
                "natural medium-length"
            ]
            choice=pick(eyelashes, 10)
            parts.append(choice + " eyelashes")

        if random_eyelid_types:
            eyelid_types = [
                "monolid",
                "double",
                "hooded",
                "semi-hooded",
                "visible crease",
                "smooth flat",
                "deep-set",
                "wide lid",
                "tapered double",
                "soft rounded"
            ]
            choice=pick(eyelid_types, 10)
            parts.append(choice + " eyelid")

        if random_nose_shapes:
            nose_shapes = [
                "straight",
                "slightly upturned",
                "button",
                "Greek",
                "Roman",
                "nubian",
                "snub ",
                "celestial",
                "aquiline",
                "soft rounded nose tip",
                "narrow nose bridge",
                "wide nose base",
                "concave profile",
                "petite straight",
                "elegant curved"
            ]
            choice=pick(nose_shapes, 10)
            parts.append(choice + " nose shape")

        if random_nose_sizes:
            nose_sizes = [
                 "small and subtle",
                 "medium balanced",
                 "slightly wide",
                 "petite narrow",
                 "slender and long",
                 "soft and rounded",
                 "refined and elegant",
                 "compact and proportionate"
            ]
            choice=pick(nose_sizes, 10)
            parts.append(choice + " nose size")

        if random_lip_shapes:
            lip_shapes = [
                "heart-shaped",
                "bow-shaped",
                "round full",
                "wide symmetrical",
                "tapered lips with pointed corners",
                "defined cupid’s bow",
                "soft oval",
                "slightly asymmetrical",
                "downturned corners ",
                "classic balanced"
            ]
            choice=pick(lip_shapes, 10)
            parts.append(choice + " lip shape")

        if random_lip_sizes:
            lip_sizes = [
                "petite",
                "medium-sized",
                "wide",
                "long but narrow",
                "short and compact",
                "full-length lips with narrow height"
            ]
            choice=pick(lip_sizes, 10)
            parts.append(choice + " lip size")

        if random_lip_fullness:
            lip_fullness = [
                "full upper and lower",
                "plump lower lip with thinner upper",
                "even medium",
                "slightly fuller upper lip",
                "natural soft",
                "subtle plump with visible definition"
            ]
            choice = pick(lip_fullness, 10)
            parts.append(choice + " lip fullness")

        if random_cheek_bones:
            cheek_bones = [
                "high and prominent",
                "soft rounded",
                "sculpted cheekbones with shadow",
                "subtle cheekbone lift",
                "defined but natural",
                "low cheekbones with wide spacing",
                "narrow and elegant",
                "angular cheekbones with contour",
                "slightly elevated",
                "youthful full"
            ]
            choice=pick(cheek_bones, 10)
            parts.append(choice + " cheekbones")

        if random_jawline:
            jawline = [
                "defined V-shaped",
                "soft rounded",
                "sharp angular",
                "slim tapered",
                "broad but smooth",
                "delicate jawline with narrow chin",
                "medium defined",
                "wide jawline with soft edges",
                "refined oval",
                "contoured yet natural"
            ]
            choice=pick(jawline, 10)
            parts.append(choice + " jawline")

        if random_chin:
            chin = [
                "soft rounded",
                "pointed",
                "subtle cleft",
                "narrow chin with taper",
                "short and delicate",
                "slightly squared",
                "refined V-shaped",
                "medium-length balanced",
                "petite chin with gentle curve",
                "elongated chin with narrow tip"
            ]
            choice=pick(chin, 10)
            parts.append(choice + " chin")

        if random_makeup_style:
            makeup_style = [
                 "natural no-makeup look with glowing skin",
                 "soft glam with rosy cheeks and nude lips",
                 "bold smokey eyes with matte nude lipstick",
                 "classic red lips with winged eyeliner",
                 "peachy monochrome makeup with soft shimmer",
                 "golden hour look with warm bronze tones",
                 "clean girl aesthetic with dewy finish and minimal makeup",
                 "vibrant eyeliner with subtle lip tint",
                 "Korean-inspired dewy skin with gradient lips",
                 "Arabian-style makeup with dramatic eyes and contour",
                 "editorial high-fashion look with sculpted cheeks and bold brows",
                 "vintage pin-up makeup with red lips and black liner flick",
                 "romantic pink eyeshadow with glossy lips",
                 "fresh spring look with pastel tones and light highlight",
                 "bronzed goddess look with full lashes and golden glow",
                 "subtle glam with champagne shimmer and pink lips",
                 "elegant evening makeup with dark eyes and soft lips",
                 "soft smoky eyes with peach lips",
                 "neutral matte tones with light contour",
                 "mauve tones with fluttery lashes and defined lips"
            ]
            choice=pick(makeup_style, 10)
            parts.append(choice + " makeup style")

        if random_beauty_marks:
            beauty_marks = [
                "freckle cluster across the nose bridge",
                "light freckles scattered over the cheeks",
                "light sun-kissed freckles across the nose and cheeks",
                "faint freckle trail from nose to cheek",
                "natural freckles with uneven spacing",
            ]
            choice=pick(beauty_marks, 10)
            parts.append(choice + "")

        parts.append(lighting)
        parts.append(camera)
        parts.append(background)

        final_prompt = ", ".join(filter(None, parts))
        return (final_prompt, seed, )


LOCAL_NODE_CLASS = {
    "InoRandomCharacterPrompt": InoRandomCharacterPrompt,
}
LOCAL_NODE_NAME = {
    "InoRandomCharacterPrompt": "Ino Random Character Prompt",
}
