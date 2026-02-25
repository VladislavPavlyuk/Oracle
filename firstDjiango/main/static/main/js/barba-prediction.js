(function () {
    if (!window.barba) {
        return;
    }

    const hud = document.getElementById("prediction-transition-hud");

    function touchesPrediction(data) {
        const fromPrediction = data.current && data.current.namespace === "prediction";
        const toPrediction = data.next && data.next.namespace === "prediction";
        return fromPrediction || toPrediction;
    }

    function animateOut(container) {
        return container.animate(
            [
                { opacity: 1, transform: "perspective(800px) rotateX(0deg) scale(1)", filter: "blur(0px)" },
                { opacity: 0, transform: "perspective(800px) rotateX(10deg) scale(0.96)", filter: "blur(6px)" }
            ],
            { duration: 420, easing: "cubic-bezier(.4,0,.2,1)", fill: "forwards" }
        ).finished;
    }

    function animateIn(container) {
        return container.animate(
            [
                { opacity: 0, transform: "perspective(800px) rotateX(-8deg) scale(1.03)", filter: "blur(8px)" },
                { opacity: 1, transform: "perspective(800px) rotateX(0deg) scale(1)", filter: "blur(0px)" }
            ],
            { duration: 560, easing: "cubic-bezier(.22,.61,.36,1)", fill: "forwards" }
        ).finished;
    }

    function pulseHud() {
        if (!hud) {
            return Promise.resolve();
        }
        hud.classList.add("is-active");
        return hud.animate(
            [
                { opacity: 0 },
                { opacity: 1, offset: 0.35 },
                { opacity: 0.6, offset: 0.7 },
                { opacity: 0 }
            ],
            { duration: 700, easing: "ease-out", fill: "forwards" }
        ).finished;
    }

    barba.init({
        transitions: [
            {
                name: "prediction-future-glitch",
                sync: true,
                custom(data) {
                    return touchesPrediction(data);
                },
                async leave(data) {
                    document.body.classList.add("is-prediction-transition");
                    await Promise.all([animateOut(data.current.container), pulseHud()]);
                },
                async enter(data) {
                    await animateIn(data.next.container);
                },
                after() {
                    document.body.classList.remove("is-prediction-transition");
                    if (hud) {
                        hud.classList.remove("is-active");
                    }
                }
            }
        ]
    });
})();
