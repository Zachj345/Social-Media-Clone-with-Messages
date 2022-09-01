$(document).ready(() => {
  let socket = io.connect("http://localhost:5000");

  socket.on("connect", () => {
    socket.send("User connected!");
    console.log("User connected!");
  });

  socket.on("message", function (message) {
    let sender = document.getElementById("sender").innerHTML;
    if (!message || typeof message === "undefined") {
      console.log("no message found");
    } else {
      console.log("message detected");
    }

    if (message != " : " && typeof message !== "undefined") {
      $("#reload").append(`<div class="card message-card"> \
            <div class="card-header">From ${sender}\
            </div> <div class="card-body me-card"> <p>${message}</p> \
                </div>
                <button
              type="button"
              aria-label="Close"
              onclick="deleteMessage({{message.id}})"
              id="del-message"
              class="btn-close delete-mess"
            ></button></div>`);
    }
    $("#reload").load(document.URL + " " + "#reload");
  });

  $("#message").keyup(function (event) {
    if (event.which === 13) {
      $("#sendBtn").click();
    }
  });

  $("#sendBtn").on("click", () => {
    socket.send($("#message").val());

    $("#message").val("");
    console.log("submit detected");
  });

  return false;
});
