function checkInp(value){
    var number = parseInt(value);
    if (!Number.isInteger(number)){
        alert("Input must be a number!");
        return false;
    }
    return true;
}

function calculate(value1,value2){
    if(checkInp(value1)){
        var number = parseInt(value1,10);
        var odds = parseFloat(value2);
        var bal = parseInt(document.getElementById("balance"));
        alert("If you win, you'll earn " + number*odds);
        return true;
    }
}