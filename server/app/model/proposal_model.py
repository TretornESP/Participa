
class ProposalModel:
    def __init__(self, id, title, description, photos, author, created_at, coordinates, likes, deleted_at, main_photo):
        self.id = id
        self.title = title
        self.description = description
        self.photos = photos
        self.author = author
        self.created_at = created_at
        self.coordinates = coordinates
        self.likes = likes
        self.deleted_at = deleted_at
        self.main_photo = main_photo

    @staticmethod
    def from_dict(source):
        return ProposalModel(
            str(source.get('_id', None)),
            source['title'],
            source['description'],
            source['photos'],
            str(source['author']),
            source['created_at'],
            source['coordinates'],
            source['likes'],
            source['deleted_at'],
            source['main_photo']
        )
    
    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_photos(self):
        return self.photos
        
    def get_author(self):
        return self.author

    def get_created_at(self):
        return self.created_at

    def get_coordinates(self):
        return self.coordinates

    def get_likes(self):
        return self.likes

    def get_deleted_at(self):
        return self.deleted_at

    def get_main_photo(self):
        return self.main_photo

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'photos': self.photos,
            'author': self.author,
            'created_at': self.created_at,
            'coordinates': self.coordinates,
            'likes': self.likes,
            'deleted_at': self.deleted_at,
            'main_photo': self.main_photo
        }

        if self.id is None:
            data.pop('id')
        return data

    def to_vo_dict(self):
        data = self.to_dict()
        data.pop('deleted_at')
        return data