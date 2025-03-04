window.onload = function () {
    const textDisplay = document.getElementById('text-display');
    const text1 = "应该怎么爱";
    const text2 = "可惜书中从无记载";
    let currentText = ""; // 用于记录当前正在显示的文本内容
    let currentIndex = 0; // 用于记录当前正在处理的文本字符索引
    let currentTextIndex = 0; // 用于标记当前正在处理的是text1还是text2，0表示text1，1表示text2
    let isGenerating = true; // 标记当前是文本生成阶段还是删除阶段
    let isText1Done = false; // 标记text1是否已经完整生成并删除过一次
    let isText2Done = false; // 标记text2是否已经完整生成并删除过一次

    function updateText() {
        if (isGenerating) {
            if (currentTextIndex === 0) {
                if (currentIndex < text1.length) {
                    currentText += text1.charAt(currentIndex);
                    currentIndex++;
                    textDisplay.innerHTML = currentText;
                } else {
                    isText1Done = true;
                    isGenerating = false;
                    currentIndex = 0;
                }
            } else {
                if (currentIndex < text2.length) {
                    currentText += text2.charAt(currentIndex);
                    currentIndex++;
                    textDisplay.innerHTML = currentText;
                } else {
                    isText2Done = true;
                    isGenerating = false;
                    currentIndex = 0;
                }
            }
        } else {
            if (currentText.length > 0) {
                currentText = currentText.slice(0, -1);
                textDisplay.innerHTML = currentText;
            } else {
                if (isText1Done && isText2Done) {
                    isText1Done = false;
                    isText2Done = false;
                }
                isGenerating = true;
                if (isText1Done &&!isText2Done) {
                    currentTextIndex = 1;
                } else {
                    currentTextIndex = 0;
                }
            }
        }
    }
    const intervalId = setInterval(updateText, 150); // 每隔150毫秒更新一次文本，可调整此间隔来改变文字生成和删除的整体速度
};