(function () {
    if (!window.barba) {
        return;
    }

    const hud = document.getElementById("prediction-transition-hud");
    const STYLE_LOAD_TIMEOUT_MS = 4000;

    function withTimeout(promise, timeoutMs) {
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => reject(new Error("Style load timeout")), timeoutMs);
            promise
                .then((value) => {
                    clearTimeout(timer);
                    resolve(value);
                })
                .catch((error) => {
                    clearTimeout(timer);
                    reject(error);
                });
        });
    }

    function waitForStylesheet(link) {
        return new Promise((resolve, reject) => {
            if (link.sheet) {
                resolve();
                return;
            }

            const onLoad = () => {
                cleanup();
                resolve();
            };

            const onError = () => {
                cleanup();
                reject(new Error("Failed to load stylesheet: " + link.href));
            };

            const cleanup = () => {
                link.removeEventListener("load", onLoad);
                link.removeEventListener("error", onError);
            };

            link.addEventListener("load", onLoad, { once: true });
            link.addEventListener("error", onError, { once: true });
        });
    }

    function getPersistentStyleHrefs() {
        return new Set(
            Array.from(document.querySelectorAll("link[rel='stylesheet'][data-persistent-style]"))
                .map((link) => link.getAttribute("href"))
                .filter(Boolean)
        );
    }

    async function syncHeadFromNextPage(nextHtml) {
        if (!nextHtml) {
            return;
        }

        const parser = new DOMParser();
        const nextDocument = parser.parseFromString(nextHtml, "text/html");
        const nextTitle = nextDocument.querySelector("title");

        if (nextTitle) {
            document.title = nextTitle.textContent;
        }

        const persistentHrefs = getPersistentStyleHrefs();
        const desiredDynamicHrefs = Array.from(nextDocument.querySelectorAll("link[rel='stylesheet']"))
            .map((link) => link.getAttribute("href"))
            .filter((href) => href && !persistentHrefs.has(href));

        const desiredSet = new Set(desiredDynamicHrefs);
        const currentDynamicLinks = Array.from(
            document.querySelectorAll("link[rel='stylesheet']:not([data-persistent-style])")
        );

        const existingByHref = new Map();
        currentDynamicLinks.forEach((link) => {
            const href = link.getAttribute("href");
            if (href && !existingByHref.has(href)) {
                existingByHref.set(href, link);
            }
        });

        const loadPromises = [];

        desiredDynamicHrefs.forEach((href) => {
            if (!existingByHref.has(href)) {
                const link = document.createElement("link");
                link.rel = "stylesheet";
                link.href = href;
                link.setAttribute("data-dynamic-style", "true");
                document.head.appendChild(link);
                existingByHref.set(href, link);
                loadPromises.push(waitForStylesheet(link));
            }
        });

        if (loadPromises.length > 0) {
            await withTimeout(Promise.all(loadPromises), STYLE_LOAD_TIMEOUT_MS);
        }

        currentDynamicLinks.forEach((link) => {
            const href = link.getAttribute("href");
            if (!href || !desiredSet.has(href)) {
                link.remove();
            }
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
                { opacity: 0, transform: "translateY(8px) scale(0.995)", filter: "blur(2px)" },
                { opacity: 1, transform: "translateY(0) scale(1)", filter: "blur(0px)" }
            ],
            { duration: 320, easing: "cubic-bezier(.22,.61,.36,1)", fill: "forwards" }
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

    barba.hooks.beforeEnter(async (data) => {
        try {
            await syncHeadFromNextPage(data.next && data.next.html);
        } catch (error) {
            window.location.assign(data.next && data.next.url ? data.next.url.href : window.location.href);
        }
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
            },
            {
                name: "default-fade",
                async leave(data) {
                    await animateOut(data.current.container);
                },
                async enter(data) {
                    await animateIn(data.next.container);
                }
            }
        ]
    });
})();
