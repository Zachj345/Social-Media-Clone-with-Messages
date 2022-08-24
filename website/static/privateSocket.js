$(document).ready(() => {
  // connect to python
  let privateSocket = io("http://localhost:5000/private");

  privateSocket.on("connect", () => {
    privateSocket.send("User connected from dms!");
    console.log("User connected from dms!");
  });
  // make sure we cant update the UI til the message is sent
  let called = false;

  $("#privateMessage").keyup(function (event) {
    if (event.which === 13) {
      $("#privateSendBtn").click();
    }
  });
  // send the username back to backend
  $("#privateSendBtn").on("click", () => {
    privateSocket.emit("username", $("#senderName").val());
    console.log("sent my username");

    let recipient = $("#privateUsername").val();
    let dm = $("#privateMessage").val();
    privateSocket.emit("username", $("#privateUsername").val().toLowerCase());
    console.log("sent second username");

    privateSocket.emit("dm", {
      username: recipient.toLowerCase(),
      message: dm,
    });

    $("#privateMessage").val("");
    console.log("submit detected");
    // now we can update
    called = true;
  });

  privateSocket.on("new_dm", (message) => {
    console.log(message);
    if (called === true) {
      console.log("called", called);
      // try to refresh

      let refresh = document.getElementById("refresh");
      $(refresh).load(document.URL + " " + `#convo-view`);
      // refreshing the convos bar to reflect a new convo that wasnt there previously
      $("#reload-convos-parent").load(document.URL + " " + "#reload-convos");

      // make sure theres an index for the UI in the case of a new conversation
      let indexes = document.querySelectorAll(".index");
      let nameTitles = [];
      let newIndex;

      // if our name isn't in here I could possibly add it(privateUsername) to this array and sort alphabetically
      // which then I could get the index of the our name in the sorted array which should be the same index
      // as is in the reload convos

      for (let i = 0; i < indexes.length; i++) {
        nameTitles.push(
          document
            .querySelector(`#title-${indexes[i].value}`)
            .innerHTML.split(" ")[20]
            .trim()
        );
        if (
          document
            .querySelector(`#title-${indexes[i].value}`)
            .innerHTML.split(" ")[20]
            .trim() === $("#privateUsername").val().trim()
        ) {
          newIndex = parseInt(indexes[i].value);
        }
      }
      if (newIndex === undefined || newIndex === null) {
        nameTitles.push($("#privateUsername").val().trim());
        nameTitles.sort();
        newIndex = nameTitles.indexOf($("#privateUsername").val().trim());
      }

      console.log(nameTitles);

      console.log(newIndex);

      // reloading elements of the UI
      let parentReload = document.querySelector(`#parentReload-${newIndex}`);
      $(parentReload).load(document.URL + " " + `#reload-${newIndex}`);

      // make sure the dm is shown again after the message is sent n the UI is 'updated'
      window.setTimeout(() => {
        for (let i = 0; i < 2; i++) {
          showDM(newIndex);
        }
      }, 80);
      // safety measure for previous case
      let conversations = document.querySelectorAll(".load-convo");
      for (let i = 0; i < conversations.length; i++) {
        if (i !== newIndex) {
          conversations[i].classList.add("hide");
          console.log(conversations[i]);
        }
      }
    }
  });
});
