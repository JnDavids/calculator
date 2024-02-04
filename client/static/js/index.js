(() => {
    const checkInputKey = (input, caretPosition) => {
        let { value } = input;
        const key = value[caretPosition - 1];

        value = value.slice(0, caretPosition - 1)
              + value.slice(caretPosition);

        if (key === "." && value.includes(".") ||
            value.replace(/\D/g, "").length === 15 && isFinite(key)
        ) {
            input.value = value;
        } else {
            return true;
        }
    };

    const formatInputNumber = e => {
        const inputLength = e.target.value.length;
        let caretPosition = e.target.selectionStart;

        if (checkInputKey(e.target, caretPosition)) {
            let value = e.target.value.replace(/[^\d.]/g, "");
            let temp = "";
            
            const decimalPointIdx = value.lastIndexOf(".");
    
            if (decimalPointIdx > -1) {
                temp = value.slice(decimalPointIdx);
                value = value.slice(0, decimalPointIdx) || "0";
            }
    
            if (value.length > 2)
                value = Number(value).toLocaleString("en");
    
            e.target.value = value + temp;
        }

        caretPosition +=  e.target.value.length - inputLength;
        e.target.setSelectionRange(caretPosition, caretPosition);
    };

    const operations = document.querySelectorAll("#operation");
    const inputValue1 = document.querySelector("#input-value-1");
    const inputValue2 = document.querySelector("#input-value-2");

    inputValue1.addEventListener("input", formatInputNumber);
    inputValue2.addEventListener("input", formatInputNumber);

    operations.forEach(operation => {
        operation.addEventListener("click", e => {
            inputValue1.value = inputValue1.value.replace(/,/g, "");
            inputValue2.value = inputValue2.value.replace(/,/g, "");
        });
    });
})();