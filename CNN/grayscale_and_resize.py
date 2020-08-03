import os
from PIL import Image

def grayScaleConverter(q):

    if not os.path.exists('./GrayScaleConverted'):
        os.mkdir('./GrayScaleConverted')

    for dirs in os.listdir(os.getcwd()+'/ScrapedImages'):
        
        if q.lower()==dirs.replace('_',' ').lower():

            if not os.path.exists(f'./GrayScaleConverted/{dirs}'):
                os.mkdir(f'./GrayScaleConverted/{dirs}')

            for images in os.listdir(os.getcwd()+f"/ScrapedImages/{dirs}"):
                img = Image.open(os.getcwd()+f'/ScrapedImages/{dirs}/{images}').convert('L')
                img.save(f'./GrayScaleConverted/{dirs}/{images}_1.jpg')

def generateThumbnail(q):
    
    for dirs in os.listdir(path='./GrayScaleConverted'):

        if q.lower()==dirs.replace('_',' ').lower():

            for images in os.listdir(f'./GrayScaleConverted/{dirs}'):
                file, ext = os.path.splitext(images)
                im = Image.open(f'./GrayScaleConverted/{dirs}/{images}')
                im.thumbnail((128,128),resample=Image.ANTIALIAS)
                file=''.join(images.split('.jpg'))
                im.save(f'./GrayScaleConverted/{dirs}/{file}_thumbnail.jpg')
                os.remove(f'./GrayScaleConverted/{dirs}/{images}')

if __name__=="__main__":
    queries=['Breaking Bad']
    for q in queries:
        grayScaleConverter(q)
        generateThumbnail(q)
