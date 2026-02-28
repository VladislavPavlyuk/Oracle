(function () {
    if (!window.barba) {
        return;
    }

    const hud = document.getElementById("prediction-transition-hud");

    function syncHeadFromNextPage(nextHtml) {
        if (!nextHtml) {
            return;
        }

        const parser = new DOMParser();
        const nextDocument = parser.parseFromString(nextHtml, "text/html");
        const nextTitle = nextDocument.querySelector("title");

        if (nextTitle) {
            document.title = nextTitle.textContent;
        }

        const persistentHrefs = new Set(
            Array.from(document.querySelectorAll("link[data-persistent-style]"))
                .map((link) => link.getAttribute("href"))
                .filter(Boolean)
        );

        document.querySelectorAll("link[rel='stylesheet']").forEach((link) => {
            if (!link.hasAttribute("data-persistent-style")) {
                link.remove();
            }
        });

        nextDocument.querySelectorAll("link[rel='stylesheet']").forEach((nextLink) => {
            const href = nextLink.getAttribute("href");
            if (!href || persistentHrefs.has(href)) {
                return;
            }

            const alreadyExists = document.querySelector(`link[rel='stylesheet'][href="${href}"]`);
            if (alreadyExists) {
                return;
            }

            const newLink = document.createElement("link");
            newLink.rel = "stylesheet";
            newLink.href = href;
            document.head.appendChild(newLink);
        });
    }

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

    barba.hooks.beforeEnter((data) => {
        syncHeadFromNextPage(data.next && data.next.html);
    });

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
