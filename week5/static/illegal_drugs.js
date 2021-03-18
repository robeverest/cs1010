function adjust_answer() {
    number = Math.floor(Math.random()*4)
    if (number == 3) {
        if (document.drugs_form.drugs.value == "yes") {
            document.drugs_form.drugs.value = "no"
        } else {
            document.drugs_form.drugs.value = "yes"
        }
    }
}