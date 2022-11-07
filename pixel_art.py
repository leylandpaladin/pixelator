import pygame as pg
import cv2
import numpy as np
import pygame.gfxdraw


class ArtConverter:
    def __init__(self, path='img/7.png', pixel_size=3, color_lvl=8):
        pg.init()
        self.path = path
        self.PIXEL_SIZE = pixel_size
        self.color_lvl = color_lvl
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        print(self.RES)
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock() 
        self.PALETTE, self.COLOR_COEFF = self.create_palette()
        

    def draw_converted_image(self):

        color_incides = self.image // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                color_key = tuple(color_incides[x,y])
                if sum(color_key):
                    color = self.PALETTE[color_key]
                    pygame.gfxdraw.box(self.surface, (x,y, self.PIXEL_SIZE,self.PIXEL_SIZE), color)

                 
    def create_palette(self):

        colors, color_coeff = np.linspace(0,255,num=self.color_lvl, dtype=int, retstep=True)
        color_palette = [np.array([r,g,b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color

        return palette, color_coeff


    def save_image(self):

        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        final_image = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite('converted_image.jpg', final_image)
        print('SAVED')


    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2GRAY)
        
        return image

    def draw_cv2_image(self):

        resized_cv2_image = cv2.resize(self.cv2_image, (800,460), interpolation = cv2.INTER_AREA)
        cv2.imshow('img', resized_cv2_image)

    def draw(self):
        
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()



    def run(self):

        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save_image()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()

if __name__ == '__main__':

    app = ArtConverter()
    app.run()
