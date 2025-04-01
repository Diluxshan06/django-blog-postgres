from django.contrib.auth.models import Group, Permission


def create_group_permissions(sender, **kwargs):
    try:
        readers, created = Group.objects.get_or_create(name="Readers")
        authors, created = Group.objects.get_or_create(name="Authors")
        editors, created = Group.objects.get_or_create(name="Editors")
    
        readers_permission = [
           Permission.objects.get(codename='view_post')
        ]
        authors_permission = [
            Permission.objects.get(codename="view_post"),
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post")
        ]
        publish, created = Permission.objects.get_or_create(codename='can_publish', content_type_id=7, name='can publish posts')
        editors_permission = [
            publish,
            Permission.objects.get(codename="view_post"),
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post")
        ]
        readers.permissions.set(readers_permission)
        authors.permissions.set(authors_permission)
        editors.permissions.set(editors_permission)
        print("Group permissions created")  
    except Exception as e:
        print(f"Error creating group permissions: {e}")  # Print the error message (e)