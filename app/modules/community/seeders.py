from app.modules.auth.models import User
from app.modules.community.models import Community
from core.seeders.BaseSeeder import BaseSeeder


class CommunitySeeder(BaseSeeder):
    def run(self):
        # Buscar al usuario 'user1@example.com'
        user = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user3@example.com').first()
        if not user:
            raise Exception("User 'user1@example.com' not found. Make sure AuthSeeder is executed first.")

        # Crear comunidades
        data = [
            Community(
                name="First Community",
                description="This is the first test community.",
                owner=user
            ),
            Community(
                name="Second Community",
                description="This is the second test community.",
                owner=user
            ),
            Community(
                name="Third Community",
                description="This is the third test community.",
                owner=user2
            )
        ]

        # Insertar comunidades en la base de datos
        communities = self.seed(data)

        # Asociar al usuario como miembro de las comunidades creadas
        for community in communities:
            community.members.append(user)
            community.members.append(user2)

        # Confirmar los cambios en la base de datos
        self.db.session.commit()

        print(f"CommunitySeeder performed successfully! {len(communities)} communities created.")