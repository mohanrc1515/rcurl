import motor.motor_asyncio
from config import Config
from .utils import send_log

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.jishubotz = self._client[database_name]
        self.col = self.Mohan_bot.user

    def new_user(self, id):
        return dict(
            _id=int(id),
            file_id=None,  # Default thumbnail
            files={},  # Changed from video_thumbnails to store all files with their thumbnails and data
            caption=None,
            prefix=None,
            suffix=None,
            metadata=False,
            metadata_code="By :- @Madflix_Bots",
            permanent_subtitle=None,  # New field for permanent subtitle
            subtitle_position="bottom",  # Default position
            subtitle_font_size=24  # Default font size
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)            
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    #======================= File Management ========================#

    async def add_file(self, id, file_id, file_data=None):
        if file_data is None:
            file_data = {}
        await self.col.update_one(
            {'_id': int(id)},
            {'$set': {f'files.{file_id}': file_data}},
            upsert=True
        )

    async def get_file_data(self, id, file_id):
        user = await self.col.find_one({'_id': int(id)})
        if user and 'files' in user and file_id in user['files']:
            return user['files'][file_id]
        return None

    async def remove_file(self, id, file_id):
        await self.col.update_one(
            {'_id': int(id)},
            {'$unset': {f'files.{file_id}': ""}}
        )

    #======================= Thumbnail Handling ========================#

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)
    
    async def set_file_thumbnail(self, id, file_id, thumbnail_id):
        await self.col.update_one(
            {'_id': int(id)},
            {'$set': {f'files.{file_id}.thumbnail': thumbnail_id}}
        )

    async def get_file_thumbnail(self, id, file_id):
        user = await self.col.find_one({'_id': int(id)})
        if user and 'files' in user and file_id in user['files']:
            return user['files'][file_id].get('thumbnail')
        return None

    #======================= Subtitle Handling ========================#

    async def set_permanent_subtitle(self, id, subtitle_text=None, subtitle_file_id=None):
        update_data = {}
        if subtitle_text:
            update_data['permanent_subtitle.text'] = subtitle_text
        if subtitle_file_id:
            update_data['permanent_subtitle.file_id'] = subtitle_file_id
        await self.col.update_one(
            {'_id': int(id)},
            {'$set': update_data}
        )

    async def get_permanent_subtitle(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('permanent_subtitle', None)

    async def clear_permanent_subtitle(self, id):
        await self.col.update_one(
            {'_id': int(id)},
            {'$unset': {'permanent_subtitle': ""}}
        )

    async def set_subtitle_settings(self, id, position=None, font_size=None):
        update_data = {}
        if position:
            update_data['subtitle_position'] = position
        if font_size:
            update_data['subtitle_font_size'] = font_size
        await self.col.update_one(
            {'_id': int(id)},
            {'$set': update_data}
        )

    #======================= Caption ========================#

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

    #======================= Prefix ========================#

    async def set_prefix(self, id, prefix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'prefix': prefix}})  
        
    async def get_prefix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('prefix', None)      

    #======================= Suffix ========================#

    async def set_suffix(self, id, suffix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'suffix': suffix}})  
        
    async def get_suffix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('suffix', None)

    #======================= Metadata ========================#
        
    async def set_metadata(self, id, bool_meta):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata': bool_meta}})
        
    async def get_metadata(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata', None)
        
    #======================= Metadata Code ========================#    
        
    async def set_metadata_code(self, id, metadata_code):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_code': metadata_code}})

    async def get_metadata_code(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_code', None)

Mohan_bot = Database(Config.DB_URL, Config.DB_NAME)
