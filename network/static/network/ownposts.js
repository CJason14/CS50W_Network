document.addEventListener('DOMContentLoaded', function () {
    loadpost()
});

function loadpost() {
    fetch('/posts/current', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(posts => {
            count = 0
            const title = document.createElement("h2");
            const title_content = document.createTextNode("Posts");
            title.appendChild(title_content);
            document.getElementById('Posts').appendChild(title);
            for (const post in posts) {
                const post_div = document.createElement("div");
                post_div.classList.add('Post');
                
                const info_div = document.createElement("div");
                const username = document.createElement("h5");
                const username_content = document.createTextNode(posts[count].creator);
                username.appendChild(username_content);
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
                const edit = document.createElement("button");
                const edit_content = document.createTextNode("Edit");
                edit.classList.add("editbutton");
                edit.appendChild(edit_content);
                const id = posts[count].id;
                const content_button = posts[count].content;
                edit.addEventListener('click', function () {
                    edit_func(id, content_button);
                })
                info_div.appendChild(username);
                info_div.appendChild(timestamp);
                info_div.appendChild(document.createElement("br"));
                info_div.appendChild(like);
                info_div.appendChild(document.createElement("br"));
                info_div.appendChild(edit);
                
                const content_div = document.createElement("div");
                const content = document.createElement("p");
                const content_content = document.createTextNode(posts[count].content)
                content.appendChild(content_content);
                content_div.appendChild(content);

                const likes_div = document.createElement("div");
                const likes_div_div = document.createElement("div");
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
}

function edit_func(id, content){
    document.getElementById('Posts').innerHTML = "";
    const title = document.createElement("h2");
    const title_content = document.createTextNode("Edit");
    title.appendChild(title_content);
    document.getElementById('Posts').appendChild(title);

    const content_textarea = document.createElement("textarea");
    const content_content = document.createTextNode(content);
    content_textarea.appendChild(content_content);
    content_textarea.classList.add("textarea");
    document.getElementById('Posts').appendChild(content_textarea);

    document.getElementById('Posts').appendChild(document.createElement("br"));

    const save = document.createElement("button");
    const save_content = document.createTextNode("Save");
    save.appendChild(save_content);
    save.classList.add("button");
    save.addEventListener('click', function () {

    });
    document.getElementById('Posts').appendChild(document.createElement("br"));
    document.getElementById('Posts').appendChild(save);
}