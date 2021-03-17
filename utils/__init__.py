def add():
    #Remove the follower and followee into the following model, if not already followed.
            new_follower = Following.objects.create(user=request.user, following=followee)
            new_follower.save()
            
            #Update the followee's followers.
            new_follow = User.objects.get(username=followee)
            new_follow.followers = new_follow.followers + 1
            new_follow.save()

            #Update the followers followed.
            new_followed = User.objects.get(username=request.user)
            new_followed.followed = new_followed.followed + 1
            new_followed.save()

def remove():
    #Remove the follower and followee into the following model, if not already followed.
            new_follower = Following.objects.create(user=request.user, following=followee)
            new_follower.save()
            
            #Update the followee's followers.
            new_follow = User.objects.get(username=followee)
            new_follow.followers = new_follow.followers - 1
            new_follow.save()

            #Update the followers followed.
            new_followed = User.objects.get(username=request.user)
            new_followed.followed = new_followed.followed - 1
            new_followed.save()

def printf():
    print("hello")