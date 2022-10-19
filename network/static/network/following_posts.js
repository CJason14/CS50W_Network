document.addEventListener('DOMContentLoaded', function () {
    loadpost()
});

let page = 1
let button_int = 0

function loadpost() {
    fetch('/posts/following', {
            method: 'POST',
            body: JSON.stringify({
                page: page
            })
        })
        .then(response => response.json())
        .then(posts => {
            count = 0
            for (const post in posts) {
                const post_div = document.createElement("div");
                post_div.classList.add('Post');

                const info_div = document.createElement("div");
                const username = document.createElement("h5");
                const username_content = document.createTextNode(posts[count].creator);
                username.appendChild(username_content);
                const link_profile = "/user/" + posts[count].creator;
                username.addEventListener("click", function (){
                    window.open(link_profile, "_self");
                    console.log("Test");
                });
                const timestamp = document.createElement("h7");
                const timestamp_content = document.createTextNode("Posted: " + posts[count].timestamp);
                timestamp.appendChild(timestamp_content);
                const like = document.createElement("h7");
                const likesall_id = '/likes/all/' + posts[count].id;
                let likes = 0;
                fetch(likesall_id, {
                        method: 'GET'
                    })
                    .then(response => response.json())
                    .then(results => {
                        likes = results.likes;
                        const like_content = document.createTextNode("Likes: " + likes);
                        like.appendChild(like_content);
                    });
                info_div.appendChild(username);
                info_div.appendChild(timestamp);
                info_div.appendChild(document.createElement("br"))
                info_div.appendChild(like);

                const content_div = document.createElement("div");
                const content = document.createElement("p");
                const content_content = document.createTextNode(posts[count].content)
                content.appendChild(content_content);
                content_div.appendChild(content);

                const likes_div = document.createElement("div");

                const likes_id = '/likes/' + posts[count].id;
                let liked = 0
                fetch(likes_id, {
                        method: 'GET'
                    })
                    .then(response => response.json())
                    .then(result => {
                        liked = result.liked;
                        if (result.liked == 1) {
                            likes_div.classList.add('heart');
                        } else {
                            likes_div.classList.add('unheart');
                        };
                        likes_div.addEventListener("click", function () {
                            if (liked == 1) {
                                liked = 0
                                likes_div.classList.remove('heart');
                                likes_div.classList.add('unheart');
                                unsetheart(likes_id);
                                likes = likes - 1;
                                like.innerHTML = "Likes: " + likes;
                            } else {
                                liked = 1
                                likes_div.classList.remove('unheart');
                                likes_div.classList.add('heart');
                                setheart(likes_id);
                                likes = likes + 1;
                                like.innerHTML = "Likes: " + likes;
                            }
                        })
                    });
                const likes_div_div = document.createElement("div");;
                likes_div_div.appendChild(likes_div);
                likes_div_div.classList.add('bottom');
                const hr = document.createElement("hr");

                post_div.appendChild(info_div);
                post_div.appendChild(hr);
                post_div.appendChild(content_div);
                post_div.appendChild(likes_div_div);

                document.getElementById('Posts').appendChild(post_div);

                count += 1
            }
        });
    if (page > 1 && button_int == 0) {
        const button = document.createElement("button");
        const content_content = document.createTextNode("Previous")
        button.appendChild(content_content);
        button.classList.add('button');
        button.addEventListener('click', function () {
            previouspage()
        });
        document.getElementById('Pages').appendChild(button);
        button_int = 1
    } else if (page == 1) {
        document.getElementById('Pages').innerHTML = "";
    }
}

function nextpage() {
    page += 1
    document.getElementById("Posts").innerHTML = "";
    loadpost();
}

function previouspage() {
    page -= 1
    document.getElementById("Posts").innerHTML = "";
    loadpost();
}

function setheart(likes_id) {
    fetch(likes_id, {
            method: 'PUT',
            body: JSON.stringify({
                liked: "True"
            })
        })
        .then(response => response.json())
        .then(result => {
        });
}

function unsetheart(likes_id) {
    fetch(likes_id, {
            method: 'PUT',
            body: JSON.stringify({
                liked: "False"
            })
        })
        .then(response => response.json())
        .then(result => {;
        });
}