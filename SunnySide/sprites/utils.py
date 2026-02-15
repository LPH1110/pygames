import pygame as pg
from sprites.spritesheet import SpriteSheet

def load_animation_strip(path, frame_count, flip_x=True, flip_y=False, scale_ratio = 1.0):
    """
    Loads a strip of images from a spritesheet and optionally creates a flipped version.
    
    Args:
        path (str): Path to the spritesheet image.
        frame_count (int): Number of frames in the strip.
        flip_x (bool): Whether to create a horizontally flipped copy.
        flip_y (bool): Whether to create a vertically flipped copy.
        
    Returns:
        tuple: (frames, frames_flipped) if flip is requested, else just frames.
               However, to keep it consistent for the player which always needs flipped,
               we can return both.
    """
    sheet = SpriteSheet(path)
    sheet_width = sheet.sheet.get_width()
    sheet_height = sheet.sheet.get_height()
    frame_width = sheet_width // frame_count
    frame_height = sheet_height
    
    frames = sheet.load_strip((0, 0, frame_width, frame_height), frame_count)
    
    if scale_ratio != 1.0:
        new_size = (int(frame_width * scale_ratio), int(frame_height * scale_ratio))
        frames = [pg.transform.scale(f, new_size) for f in frames]
    
    frames_flipped = []
    if flip_x or flip_y:
        frames_flipped = [pg.transform.flip(img, flip_x, flip_y) for img in frames]
    else:
        # If no flip requested, maybe just return empty or same?
        # For this specific refactor, we always want flipped for left/right movement.
        pass
        
    return frames, frames_flipped
