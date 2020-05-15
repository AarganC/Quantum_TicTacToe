var activePlayer = "O";
var gameType = document.getElementsByTagName('body')[0].dataset.game;

var apiUrl = "http://localhost:5000/api";
var apiAgentUrl = apiUrl + "/" + gameType;
var apiAgentStatusUrl = apiAgentUrl + "/status";
var apiAgentPlayUrl = apiAgentUrl + "/play";
var apiAgentRestartUrl = apiAgentUrl + "/restart";

window.onload = function(){
    refreshBoard();
};

$('.game-square-contents').on('click', function (e) {
    play(this.dataset.square);
    refreshBoard();
});

function play(position)
{
    // http://localhost:5000/api/basic/play?position=0

    var request = new XMLHttpRequest();
    request.open('GET', apiAgentPlayUrl + "?position=" + position);
    request.responseType = 'text';
    request.onload = function() {
        var response = JSON.parse(request.response);
        console.log(response);
        refreshBoard();
    };
    request.send();
}

function refreshBoard()
{
    var request = new XMLHttpRequest();
    request.open('GET', apiAgentStatusUrl);
    request.responseType = 'text';
    request.onload = function() {
        var response = JSON.parse(request.response);
        document.getElementById("message").innerText = response.message;
        drawBoard(response.board);
    };
    request.send();

}
function drawBoard(board)
{
    var square = 0;
    var squares = document.getElementsByClassName("game-square-contents");

    for(var rowIndex in board)
    {
        var row = board[rowIndex];

        for(var columnIndex in row)
        {
            var value = row[columnIndex];
            var currentSquare = $(squares[square]);

            if(value === -1) { currentSquare.html(''); }
            else if(value === 0) { currentSquare.html('<p>X</p>'); }
            else if(value === 1) { currentSquare.html('<p>O</p>'); }

            square++;
        }
    }
}

function restartGame()
{
    var request = new XMLHttpRequest();
    request.open('GET', apiAgentRestartUrl);
    request.responseType = 'text';
    request.onload = function() {
        var response = JSON.parse(request.response);
        console.log(response);
        refreshBoard();
    };
    request.send();
}