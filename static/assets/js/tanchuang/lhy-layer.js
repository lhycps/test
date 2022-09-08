class Promptbox {
    constructor(buttons, template) {
        this.buttons = buttons;
        this.template = template;
        this.dom = null;
        this.init();
    }

    init() {
        this.initDom();
        this.initEvent();
    }

    initDom() {
        var node = document.createElement('div');
        node.innerHTML = this.template;
        this.dom = node.childNodes[0];
    }

    initEvent() {
        // 事件
        this.dom.addEventListener('click', function (evt) {
            if (Object.keys(this.buttons).includes(evt.target.dataset.event)) {
                this.buttons[evt.target.dataset.event](this);
            }
        }.bind(this), false);

        // 动画结束
        this.dom.addEventListener('webkitAnimationEnd', function () {
            if (this.dom.classList.contains('fadein')) {
                this.dom.classList.remove('fadein')
            }
            if (this.dom.classList.contains('fadeout')) {
                this.hide()
            }
        }.bind(this), false);

        this.dom.addEventListener('animationend', function () {
            if (this.dom.classList.contains('fadein')) {
                this.dom.classList.remove('fadein')
            }
            if (this.dom.classList.contains('fadeout')) {
                this.hide()
            }
        }.bind(this), false);

    }

    fadein() {
        this.dom.classList.add('fadein')
    }

    fadeout() {
        this.dom.classList.add('fadeout')
    }

    show() {
        this.fadein();
        document.body.appendChild(this.dom);
    }

    hide() {
        document.body.removeChild(this.dom);
    }
}

class Creator {
    creator(buttons, template) {
        return new Promptbox(buttons, template);
    }
}

// 配置方法
function layer(config) {
    const {content, buttons, title, type} = config
    let layerTemplate = `<div class='layer'>
    <h2>${title}</h2>
    <p>${content}</p>
    <button  data-event="confirm">知道</button>
    <button  data-event="cancel">取消</button>
  </div>`;

    let alertTemplate = `<div class="alert alert-${type} alert-dismissible" >
    <button class="close" data-event="close"><div data-event="close"> &times;</div> </button>
    <strong>${type}!</strong> ${content}.
  </div>`

    let factory = new Creator();
    let boxUI = factory.creator(buttons, alertTemplate);
    boxUI.show();

    // // 定时器配置
    // setTimeout(() => {
    //     boxUI.fadeout()
    // }, 3000)
    return boxUI;
}