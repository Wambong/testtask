
def user_profile(request):
    if request.user.is_authenticated:
        return {
            'user_profile_pic': request.user.get_profile_pic_url()
        }
    return {}