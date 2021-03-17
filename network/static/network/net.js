function docQS(id) {
    return document.querySelector(id)
}

document.addEventListener('DOMContentLoaded', function() {
    
    let button = docQS('#follow');
    let user_to_follow = docQS('#user-name').innerHTML;
    fetch('/is_followed')
    .then(response => response.json())
    .then(followed => {
        console.log(followed)
        if(button !== null) {
        if (followed.includes(user_to_follow)) {
            
            button.value = "Unfollow"
        } else {
            
            button.value = "Follow"
        }
    }
    })
    
    if(docQS('#follow') !== null) {
    docQS('#follow').addEventListener('click', function(event) {
            event.preventDefault()
            change()
        })
    }    
})



function change() {
    let button = document.querySelector('#follow');
    let user_to_follow = docQS('#user-name').innerHTML;
    
    console.log(button)
    console.log(user_to_follow)

    fetch('/is_followed')
    .then(response => response.json())
    .then(followed => {
        console.log(followed)
        if (followed.includes(user_to_follow)) {
            follow_or_unfollow(user_to_follow)
            button.value = "Unfollow"
            window.location.href=`${user_to_follow}`;
            
        } else {
            follow_or_unfollow(user_to_follow)
            button.value = "Follow"
            window.location.href=`${user_to_follow}`;
        }
    })
}

function follow_or_unfollow(user) {
    fetch(`/follow_or_unfollow/${user}`, {
        method: 'PUT'
        })
        console.log('followee')
        
    }    
