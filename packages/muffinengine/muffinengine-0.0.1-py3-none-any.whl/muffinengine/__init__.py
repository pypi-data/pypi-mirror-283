import pygame
from pygame.locals import *
import tkinter as tk
import math
import numpy as np
import hashlib
try:
    import win32gui
except Exception:
    print("Cannot import win32gui, this probably isn't running on windows then ¯\_(ツ)_/¯")

class Window():
    def __init__(self, sizex, sizey, backgroundColor, title="MuffinEngine Window", resizeable=False, theme=0, origtheme=0):
        self.sizex = sizex
        self.sizey = sizey
        self.title = title
        self.backgroundColor = backgroundColor
        self.theme = theme
        self.origtheme = origtheme
        self.image_cache = {}
        pygame.init()
        if resizeable == True:
            self.screen = pygame.display.set_mode((self.sizex, self.sizey), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((self.sizex, self.sizey))
        pygame.display.set_caption(title)
        self.screen.fill(backgroundColor)
        self.sys = pygame

    def NextTick(self, clear=True):
        try:
            self.sys.display.flip()
            if clear:
                self.screen.fill(self.backgroundColor)
        except:
            pass
    
    def ChangeBackground(self, background):
        self.backgroundColor = self.ThemeColor(self.theme, self.origtheme, background)

    def LoadImage(self, path):
        return self.ThemeImage(self.theme, self.origtheme, self.sys.image.load(path))

    def ResizeImage(self, size, image):
        return self.sys.transform.scale(image, size)

    def RenderImage(self, pos, image):
        self.screen.blit(image, pos)

    def RenderRectangle(self, color, pos, width, height):
        rect_surface = self.sys.Surface((width, height), self.sys.SRCALPHA)
        self.sys.draw.rect(rect_surface, self.ThemeColor(self.theme, self.origtheme, color), (0, 0, width, height))
        self.screen.blit(rect_surface, pos)
    
    def RenderRectangleBatch(self, color, positions, width, height):
        for pos in positions:
            rect_surface = self.sys.Surface((width, height), self.sys.SRCALPHA)
            self.sys.draw.rect(rect_surface, self.ThemeColor(self.theme, self.origtheme, color), (0, 0, width, height))
            self.screen.blit(rect_surface, pos)

    def RenderRectangleBatchComplex(self, colors, positions, sizes):
        for i in range(len(positions)):
            pos = positions[i]
            color = colors[i]
            size = sizes[i]
            rect_surface = self.sys.Surface(size, self.sys.SRCALPHA)
            self.sys.draw.rect(rect_surface, self.ThemeColor(self.theme, self.origtheme, color), (0, 0, size[0], size[1]))
            self.screen.blit(rect_surface, pos)

    def RenderRoundedRectangle(self, color, pos, width, height, radius):
        try:
            self.RenderRectangle(color, (pos[0]+radius, pos[1]), width-radius*2, height)
            self.RenderRectangle(color, (pos[0], pos[1]+radius), width, height-radius*2)
            self.RenderCircle((pos[0]+radius, pos[1]+radius), radius, color)
            self.RenderCircle((pos[0]+radius+width-radius*2, pos[1]+radius), radius, color)
            self.RenderCircle((pos[0]+radius, pos[1]+radius+height-radius*2), radius, color)
            self.RenderCircle((pos[0]+radius+width-radius*2, pos[1]+radius+height-radius*2), radius, color)
        except pygame.error:
            pass

    def RenderLine(self, startpos, endpos, color, thickness):
        self.sys.draw.line(self.screen, self.ThemeColor(self.theme, self.origtheme, color), startpos, endpos, thickness)
    
    def RenderCircle(self, pos, radius, color):
        rect_surface = self.sys.Surface((self.sizex, self.sizey), self.sys.SRCALPHA)
        self.sys.draw.circle(rect_surface, self.ThemeColor(self.theme, self.origtheme, color), pos, radius)
        self.screen.blit(rect_surface, (0,0))
    
    def RenderCircleBatch(self, positions, radius, color):
        rect_surface = self.sys.Surface((self.sizex, self.sizey), self.sys.SRCALPHA)
        for pos in positions:
            self.sys.draw.circle(rect_surface, self.ThemeColor(self.theme, self.origtheme, color), pos, radius)
        self.screen.blit(rect_surface, (0, 0))

    def RenderText(self, text, antialias, color, size, pos, font_path=None):
        custom_font = self.sys.font.Font(font_path, int(round(size)))
        text_surface = custom_font.render(text, antialias, self.ThemeColor(self.theme, self.origtheme, color))
        self.screen.blit(text_surface, pos)
    
    def RenderPolygon(self, vert_list, color):
        rect_surface = self.sys.Surface((self.sizex, self.sizey), self.sys.SRCALPHA)
        self.sys.draw.polygon(rect_surface, self.ThemeColor(self.theme, self.origtheme, color), vert_list)
        self.screen.blit(rect_surface, (0,0))
    
    def CreateButton(self, position, width, height, clickfunction, args, hoverreturn=(127,127,127), nohoverreturn=(0,0,0), clickreturn=(255,255,255)):
        pos = self.GetMousePos()
        if pos[0] >= position[0] and pos[1] >= position[1]:
            if pos[0] <= position[0]+width and pos[1] <= position[1]+height:
                if self.GetMouseDown():
                    clickfunction(*args)
                    return clickreturn
                return hoverreturn
        return nohoverreturn

    def ThemeColor(self, mode, originalmode, color):
        if mode == originalmode:
            return color
        else:
            return (255-color[0], 255-color[1], 255-color[2])
    
    def hash_image(self, image):
        """Generate a hash for the image."""
        pixel_data = pygame.image.tostring(image, 'RGBA')
        return hashlib.sha256(pixel_data).hexdigest()

    def ThemeImage(self, mode, originalmode, image):
        if mode == originalmode:
            return image
        else:
            image_hash = self.hash_image(image)
            if image_hash in self.image_cache:
                return self.image_cache[image_hash]
            image = image.convert_alpha()
            width, height = image.get_size()
            inverted_image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.lock()
            inverted_image.lock()
            for x in range(width):
                for y in range(height):
                    r, g, b, a = image.get_at((x, y))
                    inverted_image.set_at((x, y), (255 - r, 255 - g, 255 - b, a))
            image.unlock()
            inverted_image.unlock()
            self.image_cache[image_hash] = inverted_image
            return inverted_image

    def GetMousePos(self):
        return self.sys.mouse.get_pos()
    
    def GetMouseDown(self, btn=0):
        return self.sys.mouse.get_pressed()[btn]
    
    def ChangePos(self, pos):
        try:
            win32gui.SetWindowPos(win32gui.FindWindow(None, self.title), 0, pos[0], pos[1], self.sizex, self.sizey, 0)
        except Exception as e:
            print("The window position changing function currently only works on Windows operating systems.")

class TkinterWindow():
    def __init__(self, title, size, backgroundColor):
        self.title = title
        self.backgroundColor = backgroundColor
        self.size = size
        self.window = tk.Tk()
        self.window.title(title)
        self.window.configure(bg=backgroundColor)
        self.window.geometry(str(size[0])+"x"+str(size[1]))
        self.sys = tk
    
    def CreateLabel(self, text):
        label = tk.Label(self.window, text=text)
        label.pack()
        return label
    
    def CreateTextbox(self):
        textbox = tk.Entry(self.window)
        textbox.pack()
        return textbox
    
    def CreateButton(self, text, function):
        button = tk.Button(self.window, text=text, command=function)
        button.pack()
        return button
    
    def StartLoop(self):
        self.window.mainloop()

class Settings():
    def __init__(self):
        self.tmp = "tmp"
    
    def GetKeybindForKey(self, key):
        return key

class Renderer3d():
    def __init__(self, window, focal_length):
        self.window = window
        self.focal_length = focal_length
        self.camera_position = (0, 0, 0)
        self.camera_rotation = (0, 0, 0)

    def set_camera(self, position, rotation):
        self.camera_position = position
        self.camera_rotation = rotation
    
    def RotateVert(self, vertex, origin, angle_x=0, angle_y=0, angle_z=0):
        x, y, z = vertex

        translated_x = x
        translated_y = y
        translated_z = z

        angle_x = math.radians(angle_x)
        angle_y = math.radians(angle_y)
        angle_z = math.radians(angle_z)

        rotation_x = [
            [1, 0, 0],
            [0, math.cos(angle_x), -math.sin(angle_x)],
            [0, math.sin(angle_x), math.cos(angle_x)]
        ]

        rotation_y = [
            [math.cos(angle_y), 0, math.sin(angle_y)],
            [0, 1, 0],
            [-math.sin(angle_y), 0, math.cos(angle_y)]
        ]

        rotation_z = [
            [math.cos(angle_z), -math.sin(angle_z), 0],
            [math.sin(angle_z), math.cos(angle_z), 0],
            [0, 0, 1]
        ]

        rotated_x, rotated_y, rotated_z = translated_x, translated_y, translated_z

        for rotation_matrix in [rotation_x, rotation_y, rotation_z]:
            rotated_x_new = (
                rotation_matrix[0][0] * rotated_x +
                rotation_matrix[0][1] * rotated_y +
                rotation_matrix[0][2] * rotated_z
            )

            rotated_y_new = (
                rotation_matrix[1][0] * rotated_x +
                rotation_matrix[1][1] * rotated_y +
                rotation_matrix[1][2] * rotated_z
            )

            rotated_z_new = (
                rotation_matrix[2][0] * rotated_x +
                rotation_matrix[2][1] * rotated_y +
                rotation_matrix[2][2] * rotated_z
            )

            rotated_x, rotated_y, rotated_z = rotated_x_new, rotated_y_new, rotated_z_new

        return (rotated_x, rotated_y, rotated_z)

    def RotateVerts(self, vert_list, origin, degreestuple):
        new_vert_list = []
        for vert in vert_list:
            new_vert_list.append(self.RotateVert(origin, degreestuple[0], degreestuple[1], degreestuple[2]))
        return new_vert_list
    
    def MoveVerts(self, vert_list, newpos):
        new_vert_list = []
        for vert in vert_list:
            x, y, z = vert
            xoffset, yoffset, zoffset = newpos
            new_x = x + xoffset
            new_y = y + yoffset
            new_z = z + zoffset
            new_vert_list.append((new_x, new_y, new_z))
        return new_vert_list

    def RenderObjectOld(self, edge_list, vert_list):
        new_vert_list = []
        i = 0
        for vert in vert_list:
            x = vert[0]
            y = vert[1]
            z = vert[2]
            x_projected = (self.focal_length * x) / (self.focal_length + z) + self.window.sizex / 2
            y_projected = (self.focal_length * y) / (self.focal_length + z) + self.window.sizey / 2
            new_vert_list.append((x_projected, y_projected))
            i += 1
        
        for edge in edge_list:
            self.window.RenderLine(new_vert_list[edge[0]], new_vert_list[edge[1]], (0,0,0), 1)
    
    def RenderObject(self, edge_list, vert_list, face_list):
        new_vert_list = []
        i = 0
        for vert in vert_list:
            x, y, z = vert
            x -= self.camera_position[0]
            y -= self.camera_position[1]
            z -= self.camera_position[2]

            x, y, z = self.RotateVert((x, y, z), (0, 0, 0), *self.camera_rotation)

            x_projected = (self.focal_length * x) / (self.focal_length + z) + self.window.sizex / 2
            y_projected = (self.focal_length * y) / (self.focal_length + z) + self.window.sizey / 2
            new_vert_list.append((x_projected + self.camera_position[0], y_projected + self.camera_position[1]))
            i += 1

        for face in face_list:
            self.window.RenderPolygon([new_vert_list[index] for index in face], (255,0,0))
        
        for edge in edge_list:
            self.window.RenderLine(new_vert_list[edge[0]], new_vert_list[edge[1]], (0, 0, 0), 1)
    
    def GenerateFaceList(self, vert_list, edge_list):
        faces = []
        edges_by_vert = {i: set() for i in range(len(vert_list))}
        for edge in edge_list:
            edges_by_vert[edge[0]].add(edge)
            edges_by_vert[edge[1]].add(edge)
        visited_edges = set()
        for edge in edge_list:
            if edge in visited_edges:
                continue
            face = []
            current_edge = edge
            while True:
                face.append(current_edge[0])
                visited_edges.add(current_edge)
                next_edges = edges_by_vert[current_edge[0]].union(edges_by_vert[current_edge[1]])
                next_edges.discard(current_edge)
                next_edge = next(iter(next_edges))
                if next_edge == edge:
                    break
                current_edge = next_edge
            faces.append(face)
        return faces
