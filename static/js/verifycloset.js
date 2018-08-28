"use strict";

function savePieceDetails(thing) {
    
    let $inputs= $(`#form-${thing} :input`);

    console.log($inputs);

    // for creating a list of category checkboxes
    let categoryString = "";

    $(".category-field:checked").each(function() {
        categoryString += "," + ($(this).val());
    });

    console.log(categoryString);

    let formInputs = {
        "desc": $(".desc-field").val(),
        "other_desc": $(".other-desc-field").val(),
        "clothing_type": $(".clothing-type-field").val(),
        "category": categoryString,
    };

    console.log(formInputs);

    console.log(formInputs.category);

    $.post("/verifycloset", formInputs, function() {
        alert("woo it worked? maybe?");
    });

};
