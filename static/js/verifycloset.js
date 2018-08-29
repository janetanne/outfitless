"use strict";

function flashSaved(result) {
    $(`#form-${result}`).removeClass("visible").addClass("hidden");
    $(`#div-${result}`).removeClass("hidden").addClass("visible");
};

function savePieceDetails(thing) {

    // creates list of all elements in form
    let formInputs= $(`#form-${thing}`).serialize();

    $.ajax({
        type: "POST",
        url: '/verifycloset',
        data: formInputs,
        dataType: "json",
        success: flashSaved()
    });
}
    // $.post("/verifycloset", formInputs, flashSaved);
