function $(id) {
    return document.getElementById(id);
}

function increase() {
    $('counter').value = parseInt($('counter').value) + 1;
}

function decrease() {
    var counterValue = parseInt($('counter').value);
    var newCounterValue = (counterValue)
        ? counterValue - 1
        : 0;

    $('counter').value = newCounterValue;
}