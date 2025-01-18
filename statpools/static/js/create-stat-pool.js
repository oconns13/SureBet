
function SetGame(num) { 
	var gameDropdown = document.getElementById("selectedGame")
    var gameInput = document.getElementById("gameSelectedInput")
    var games = document.getElementById("games")

    var gamesList = JSON.parse(games.value.replaceAll("\'", "\"").replaceAll("Timestamp(", "").replaceAll(")", ""))
    gameInput.value = JSON.stringify(gamesList[num])

    gameDropdown.innerHTML = "<div class='game-desc'>" +
                             "<img src='"+gamesList[num].alogo+"' height='30' width='30'/>" +
                             "<b>"+gamesList[num].away+" @</b>" +
                             "<img src='"+gamesList[num].hlogo+"' height='30' width='30'/>"+
                             "<b>"+gamesList[num].home+"</b></div><div class='game-date'>"+
                             ""+gamesList[num].date+"</div>"

    document.getElementById('gameMenu').classList.toggle("show");
    TogglePlayerDropdown(false)
    ToggleStatDropdown(true)
    ResetPlayer()
    return GetPlayerOptions(gamesList[num])
}


function GetPlayerOptions(game) {
    var options = []
	$.ajax({
		type: 'GET',
		url: 'create/addcategory/players/'+game.id,
		async: false,
		success: function(response) {
            var playerDropdown = document.getElementById("player-dropdown-menu")
            playerDropdown.innerHTML = ""
			const data = response.data
            options = data
			data.map(item=>{
                var player_ref = item.id +"|"+ item.pos +"|"+ item.num +"|"+ item.name +"|"+ item.img
                var itemHTML = "<a class='dropdown-item' onclick='SetPlayer(\""+player_ref+"\")'>" +
                             "<img src='"+item.img+"' height='40' width='50'/>" + 
                             "<div style='display: inline-block;'>" +
                             "<div style='margin:auto; text-align: center;'>" +
                             "#"+item.num+"<b>\t\t"+item.name+"</b></div> "+item.pos+"</div></a>"
                
                playerDropdown.innerHTML += itemHTML
			})
		}
	})
    return options
}

function SetPlayer(player) {
    var playerSplit = player.split("|")
	var playerDropdown = document.getElementById("selectedPlayer")
    var playerInput = document.getElementById("playerSelectedInput")

    playerInput.value = player
    playerDropdown.innerHTML = "<div style='display: inline-block; text-align: center;'>" +
                                "<img src='"+playerSplit[4]+"' height='40' width='50'/>" +
                                "<div style='display: inline-block; text-align:left;'>" +
                                "<div style='margin:auto;'>" +
                                "#"+playerSplit[2]+"<b>\t\t"+playerSplit[3]+"</b></div>"+playerSplit[1]+
                                "</div></div>"
    
    document.getElementById('player-dropdown-menu').classList.toggle("show");
    ToggleStatDropdown(false)
    ResetStat()
    GetStatOptions(playerSplit[1])
}

function GetStatOptions(player) {
	$.ajax({
		type: 'GET',
		url: 'create/addcategory/stat/'+player,
		async: false,
		success: function(response) {
            var statDropdown = document.getElementById("stat-dropdown-menu")
            statDropdown.innerHTML = ""
			const data = response.data
			data.map(item=>{
                var itemHTML = "<a class='dropdown-item' style='text-align:center;'" +
                             "onclick='SetStat(\""+item.key+"\",\""+item.desc+"\")'>" +"<b>" + item.desc + "</b></a>"
                statDropdown.innerHTML += itemHTML
			})
		}
	})
}

function SetStat(statKey, statDesc) {
	var statDropdown = document.getElementById("selectedStat")
    var statInput = document.getElementById("statSelectedInput")
    var btn = document.getElementById("add_category_submit_btn")

    document.getElementById('stat-dropdown-menu').classList.toggle("show");
    statInput.value = statKey
    statDropdown.innerHTML = "<b>" + statDesc + "</b>"
    btn.disabled = false
}

function ResetPlayer() {
    var playerDropdown = document.getElementById("selectedPlayer")
    var playerInput = document.getElementById("playerSelectedInput")
    playerInput.value = null
    playerDropdown.innerHTML = "CHOOSE A PLAYER"

    ResetStat()
}

function ResetStat() {
    var statDropdown = document.getElementById("selectedStat")
    var statInput = document.getElementById("statSelectedInput")
    var btn = document.getElementById("add_category_submit_btn")

    statInput.value = null
    statDropdown.innerHTML = "CHOOSE A STATISTIC"
    btn.disabled = true
}

function TogglePlayerDropdown(disabled) {
    var playerButton = document.getElementById("playerDropdown")
    playerButton.disabled = disabled
}

function ToggleStatDropdown(disabled) {
    var statButton = document.getElementById("statDropdown")
    statButton.disabled = disabled
}

function CloseWindow(shouldRefresh) {
    var catModal = document.getElementById("popupModal")
    catModal.innerHTML = ""
    if (shouldRefresh) {
        window.location.reload()
    }
}

function Shuffle() {
    var games = document.getElementById("games")
    var gamesList = JSON.parse(games.value.replaceAll("\'", "\"").replaceAll("Timestamp(", "").replaceAll(")", ""))
    var randomGameNum = Math.floor(Math.random() * gamesList.length)
    
    var players = SetGame(randomGameNum)

    var randomNum = Math.floor(Math.random() * players.length)
    player_ref = players[randomNum].id +"|"+ players[randomNum].pos +"|"+ players[randomNum].num +"|"+ players[randomNum].name +"|"+ players[randomNum].img
    
    SetPlayer(player_ref)
}

function ShowOptions(id) {
    if (id != "gameMenu") {
        document.getElementById("gameMenu").classList.remove("show");
    }
    if (id != "player-dropdown-menu") {
        document.getElementById("player-dropdown-menu").classList.remove("show");
    }
    if (id != "stat-dropdown-menu") {
        document.getElementById("stat-dropdown-menu").classList.remove("show");
    }
    document.getElementById(id).classList.toggle("show");
  }