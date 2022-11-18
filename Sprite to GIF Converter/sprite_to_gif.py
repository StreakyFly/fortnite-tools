from PIL import Image, ImageFont, ImageDraw
import numpy as np
import math
import glob
import os


# TODO change these locations to your own
save_to = "C:/Users/USER/Desktop/FModel/ReadyToPost/EmojiGIFs"  # where the final GIFs will be saved
from_path = "C:/Users/USER/Desktop/Solitude-master/Solitude/bin/Debug/net6.0/Files/Output/2dAssets"  # where should it check for Sprites
cropped_sprite_folder = "C:/Users/USER/fakulteta/programiranje1/Bots/Fortnite Datamining/Sprite to GIF/sprite_pieces"  # the location for temporarily saving sprite pieces
frames_folder = "C:/Users/USER/fakulteta/programiranje1/Bots/Fortnite Datamining/Sprite to GIF/frames"  # the location for temporarily saving frame images


def main():
    sprites = []
    imgs_all = glob.glob(f"{from_path}/*")
    for i in imgs_all:
        if i.endswith("_Sprite.png") or i.endswith("_Sprites.png"):
            sprites.append(i)

    for num, sprite in enumerate(sprites, start=1):
        print("Converting", sprite.split("\\")[-1])
        img = add_sprite_backgroud(filename=sprite)
        crop(img=img, x_axis=4, y_axis=4, num=num)
        pngs_to_gif(sprite, cropped_sprite_folder, which=num)

    merge_sprite_pieces(sprites)
    pngs_to_gif("MERGED", frames_folder, which=0)
    delete_files(cropped_sprite_folder)
    delete_files(frames_folder)

    print("Complete.")


def add_sprite_backgroud(filename):
    fg = Image.open(filename)
    fgx, fgy = fg.size
    bg = Image.new("RGBA", (fgx, fgy), (40, 40, 40))
    bg.paste(fg, (0, 0), fg)
    return bg


def crop(img, x_axis, y_axis, num):
    w, h = img.size
    w_unit = w // x_axis
    h_unit = h // y_axis
    count = 1
    for y in range(y_axis):
        for x in range(x_axis):
            sprite_piece = img.crop((w_unit * x,
                                     h_unit * y,
                                     w_unit * (x + 1),
                                     h_unit * (y + 1)))

            str_count = count if count >= 10 else f"0{count}"
            str_num = num if num >= 10 else f"0{num}"
            sprite_piece.save(f"{cropped_sprite_folder}/n{str_num}_p{str_count}.png")
            count += 1


def pngs_to_gif(filename, img_folder, which):
    frames = []
    imgs = glob.glob(f"{img_folder}/*.png")
    if which == 0:
        pass
    else:
        str_num = f"n{which}" if which >= 10 else f"n0{which}"
        imgs = [i for i in imgs if str_num in i]

    for i in imgs:
        frames.append(Image.open(i))

    if "\\" in filename:
        filename = filename.split("\\")[-1]
    name = filename.split("_Sprite")[0]
    frames[0].save(f"{save_to}/{name}.gif",
                   format='GIF',
                   append_images=frames,
                   save_all=True,
                   duration=100, loop=0)


def merge_sprite_pieces(sprites):
    print("Merging frames...")
    sprite_count = len(sprites)
    imgs = glob.glob(f"{cropped_sprite_folder}/*.png")
    sprite_pieces_per_sprite = len([i for i in imgs if "n01" in i])
    x_count = round(math.sqrt(sprite_count))
    y_count = int(sprite_count / x_count) if sprite_count % x_count == 0 else int(sprite_count / x_count) + 1

    for num, spps in enumerate(range(sprite_pieces_per_sprite), start=1):
        frame = []
        id = num if num >= 10 else f"0{num}"
        for i in imgs:
            if f"p{id}" in i:
                frame.append(i)

        if len(sprites) == 3:
            y_count = 3
        grid_img = pil_grid(images=frame, max_horiz=y_count)
        W, H = grid_img.size

        draw = ImageDraw.Draw(grid_img)
        font = ImageFont.truetype("BurbankBigRegular-Bold.otf", 20)
        text = "Generated by StreakyFly"
        _, _, w, h = draw.textbbox((0, 0), text, font=font)
        draw.text(((W - w) / 2, H-26), text, (240, 240, 240), font=font)

        grid_img.save(f"{frames_folder}/frame_{id}.png")


def pil_grid(images, max_horiz=np.iinfo(int).max):
    MARGIN = 30
    BOTTOM_EXTRA_MARGIN = 20

    images = [Image.open(i) for i in images]
    n_images = len(images)
    n_horiz = min(n_images, max_horiz)  # rows
    h_sizes, v_sizes = [0] * n_horiz, [0] * ((n_images // n_horiz) + (1 if n_images % n_horiz > 0 else 0))
    for i, im in enumerate(images):
        h, v = i % n_horiz, i // n_horiz
        h_sizes[h] = max(h_sizes[h], im.size[0])
        v_sizes[v] = max(v_sizes[v], im.size[1])

    h_sizes, v_sizes = np.cumsum([0] + h_sizes), np.cumsum([0] + v_sizes)
    columns = int(n_images/n_horiz) if n_images/n_horiz < n_horiz and n_images % n_horiz else int(n_images/n_horiz) - 1
    im_grid = Image.new('RGBA', (h_sizes[-1]+(n_horiz-1)*MARGIN + MARGIN*2, v_sizes[-1]+columns*MARGIN + MARGIN*2 + BOTTOM_EXTRA_MARGIN), color=(40, 40, 40))
    #                                        margin between gifs  margin left, right    marg. bet. gifs  margin top, bottom
    for i, im in enumerate(images):
        im_grid.paste(im, (h_sizes[i % n_horiz] + MARGIN*(i % n_horiz) + MARGIN, v_sizes[i // n_horiz] + MARGIN*(i // n_horiz) + MARGIN))
        #                                         margin between gifs    margin around                   margin between gifs     margin around
    return im_grid


def delete_files(location):
    print(f"Deleting files in \"{'/'.join(location.split('/')[-2:])}\"")
    files = glob.glob(f"{location}/*")
    for f in files:
        os.remove(f)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
