window.onload = () => {
  const mediaQuery = window.matchMedia("(max-width:840px)");
  let offCanvas = document.querySelectorAll(".offcanvas");

  mediaQuery.addEventListener("change", (event) => {
    if (event.matches) {
      for (let i = 0; i < offCanvas.length; i++) {
        offCanvas[i].classList.remove("offcanvas-end");
        offCanvas[i].classList.add("offcanvas-top");
      }
    }
  });
};

function hideComment(postId) {
  let commentForm = document.querySelector(`#comment-form-${postId}`);
  if (!commentForm.classList.contains("hide")) {
    commentForm.classList.add("hide");
  }
}

function showComment(postId) {
  let commentForm = document.querySelector(`#comment-form-${postId}`);

  if (commentForm.classList.contains("hide")) {
    commentForm.classList.remove("hide");
  } else {
    commentForm.classList.add("hide");
  }
}

function showDM(index) {
  let conversations = document.querySelectorAll(".load-convo");

  for (i = 0; i < conversations.length; i++) {
    if (conversations[i].classList.contains("hide") && i === index) {
      conversations[i].classList.remove("hide");

      let title = document.getElementById(`title-${index}`).innerHTML;
      let currentUname = title.split(" ")[20];

      $("#privateUsername").val(currentUname);
    } else {
      conversations[i].classList.add("hide");
    }
  }
  console.log("show DM function called with index " + index);
}

function addComment(postId) {
  console.log("called add function");

  let comment = document.getElementById(`comment-${postId}`).value;

  let searchData = new URLSearchParams();
  searchData.append("comment", comment);
  fetch(`/add-comment/${postId}`, { method: "POST", body: searchData })
    .then((res) => res.json())
    .then((data) => {
      let canvas = document.getElementById(`offcanvasBody-${data.postId}`);
      $(canvas).load(document.URL + " " + `#offcanvasBody-${data.postId}`);
      $(".comment-box").val("");
    })
    .catch((e) => alert("Sorry, can't post this comment"));
  return false;
}

function deleteMessage(messageId) {
  fetch(`/unsend-chat-message/${messageId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      let canvas = document.getElementById("reload");
      $(canvas).load(document.URL + " " + `#reload`);
    })
    .catch((e) => alert(e));
  return false;
}

function deleteDM(messageId, index) {
  console.log(index);

  fetch(`/unsend-message/${messageId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      let refresh = document.getElementById("refresh");

      let parentReload = document.querySelector(`#parentReload-${index}`);

      $(refresh).load(document.URL + " " + `#convo-view`);
      $(parentReload).load(document.URL + " " + `#reload-${index}`);

      $("#reload-convos-parent").load(document.URL + " " + "#reload-convos");

      window.setTimeout(() => {
        for (let i = 0; i < 2; i++) {
          showDM(index);
        }
      }, 50);
      let conversations = document.querySelectorAll(".load-convo");
      for (let i = 0; i < conversations.length; i++) {
        if (i !== index) {
          conversations[i].classList.add("hide");
          console.log(conversations[i]);
        }
      }
    })
    .catch((e) => console.log(e));

  return false;
}

function deleteComment(commentId) {
  fetch(`/delete-comment/${commentId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      let canvas = document.getElementById(`offcanvasBody-${data.postId}`);
      $(canvas).load(document.URL + " " + `#offcanvasBody-${data.postId}`);
    })
    .catch((e) => console.log(e));
  return false;
}

function deletePost(postId) {
  let refreshPost = document.getElementById(`posts`);

  fetch(`/delete-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      $(refreshPost).load(document.URL + " " + "#posts");
    })
    .catch((e) => console.log(e));
  return false;
}

function like(postId) {
  const likeButton = document.getElementById(`like-btn-${postId}`);
  const likeCount = document.getElementById(`like-count-${postId}`);

  fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = `&nbsp;: ${data.likes}`;

      if (data.liked === true) {
        likeButton.className = "fa-solid fa-heart fa-2x heart";
      } else {
        likeButton.className = "fa-regular fa-heart fa-2x heart";
      }
    })
    .catch((e) => console.log(e));
}
