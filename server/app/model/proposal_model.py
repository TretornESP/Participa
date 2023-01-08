
class ProposalModel:
    def __init__(self, id, title, description, photos, author, created_at, likes):
        self.id = id
        self.title = title
        self.description = description
        self.photos = photos
        self.author = author
        self.created_at = created_at
        self.likes = likes

    @staticmethod
    def from_dict(source):
        return ProposalModel(
            str(source.get('_id', None)),
            source['title'],
            source['description'],
            source['photos'],
            source['author'],
            source['created_at'],
            source['likes']
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

    def get_likes(self):
        return self.likes

    def to_dict(self):


        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'photos': self.photos,
            'author': self.author,
            'created_at': self.created_at,
            'likes': self.likes
        }

        if self.id is None:
            data.pop('id')
        
        return data

    def to_vo_dict(self):
        data = self.to_dict()
        data.pop('author')
        return data