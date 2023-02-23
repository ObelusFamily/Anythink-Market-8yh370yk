from slugify import slugify
import requests
import os
from app.db.errors import EntityDoesNotExist
from app.db.repositories.items import ItemsRepository
from app.models.domain.items import Item
from app.models.domain.users import User


async def check_item_exists(items_repo: ItemsRepository, slug: str) -> bool:
    try:
        await items_repo.get_item_by_slug(slug=slug)
    except EntityDoesNotExist:
        return False

    return True


def get_slug_for_item(title: str) -> str:
    return slugify(title)


def check_user_can_modify_item(item: Item, user: User) -> bool:
    return item.seller.username == user.username

def get_dalle_default_image(title: str) -> dict:
    url = "https://api.openai.com/v1/images/generations"
    headers = {'Authorization':'Bearer '+ os.getenv('OPEN_API_KEY')}
    params = {
        'prompt': title
    }
    with requests.Session() as s:
        response = s.post(url,headers=headers,params=params)
        if response.ok:
            gen_image = response.json()
        else:
            raise Exception(response.text)
    
    image_url = gen_image['data'][0]['url']
    return image_url