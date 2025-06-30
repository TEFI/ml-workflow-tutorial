function validateForm() {
    const form = document.forms["trainForm"];
    const nEstimators = form["n_estimators"].value;
    const maxDepth = form["max_depth"].value;

    if (nEstimators < 1 || nEstimators > 1000) {
        alert("Number of estimators must be between 1 and 1000");
        return false;
    }
    if (maxDepth < 1 || maxDepth > 100) {
        alert("Max depth must be between 1 and 100");
        return false;
    }
    return true;
}
