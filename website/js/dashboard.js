window.onload = () => {
    const fragment = new URLSearchParams(window.location.hash.slice(1));
    
    if (fragment.has("access_token")) {
        const accessToken = fragment.get("access_token");
        const tokenType = fragment.get("token_type");

        fetch('https://discordapp.com/api/users/@me', {
            headers: {
                authorization: `${tokenType} ${accessToken}`
            }
        })
            .then(res => res.json())
            .then(response => {
                console.log(response)
                const { username, discriminator,servers } = response;
                console.log(` ${username}#${discriminator}`)
                usernameDOM = document.getElementById('username')
                        var newEl = document.createElement('p')
                        newEl.innerHTML = '<p>' +` ${username}` + ' <a href = "https://discordapp.com/api/oauth2/authorize?client_id=525814724567367682&redirect_uri=http%3A%2F%2Flocalhost%2FRAM%2Fdashboard.html&response_type=token&scope=identify%20guilds">Not you?</a></p> '
                        usernameDOM.appendChild(newEl)
            })
            .catch(console.error);
            fetch('https://discordapp.com/api/users/@me/guilds', {
            headers: {
                authorization: `${tokenType} ${accessToken}`
            }
        })
            .then(res => res.json())
            .then(response => {
                console.log(response)
                var oReq = new XMLHttpRequest();
                oReq.addEventListener("load", reqListener);
                oReq.send();
                for (i = 0; i < response.length; i++) {
                    if (response[i].permissions == "2146959359") {
                    console.log(response[i].name)
                    var newEl = document.createElement('a')
                    newEl.innerHTML = '<a class= "server'+ i +  '"href = "https://discordapp.com/api/oauth2/authorize?client_id=525814724567367682&redirect_uri=http%3A%2F%2Flocalhost%2FRAM%2Fdashboard.html&response_type=token&scope=identify%20guilds">' + response[i].name +'</a>'
                    serverDOM = document.getElementById('myDropdown')
                    serverDOM.appendChild(newEl)
                    function reqListener () {
                        console.log(this.responseText);
                      }
                      

                }
            }
                
            })
            .catch(console.error);

    }
    else {
        usernameDOM = document.getElementById('username')
        var newEl = document.createElement('p')
        newEl.innerHTML = '<a href = "https://discordapp.com/api/oauth2/authorize?client_id=525814724567367682&redirect_uri=http%3A%2F%2Flocalhost%2FRAM%2Fdashboard.html&response_type=token&scope=identify%20guilds">Login</a> '
        usernameDOM.appendChild(newEl)
    }
}