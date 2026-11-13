import os

from playwright.sync_api import expect


class DemoHelper:

    @staticmethod
    def is_enabled():
        return os.getenv("DEMO_MODE") == "1"

    @staticmethod
    def highlight(page, locator):
        if not DemoHelper.is_enabled():
            return

        DemoHelper.hide_demo_overlay(page)

        locator.scroll_into_view_if_needed()

        locator.evaluate(
            """
            element => {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            }
            """
        )

        page.wait_for_timeout(120)

        locator.evaluate(
            """
            element => {
                element.dataset.originalOutline =
                    element.style.outline;

                element.dataset.originalOutlineOffset =
                    element.style.outlineOffset;

                element.style.outline =
                    '4px solid red';

                element.style.outlineOffset =
                    '3px';
            }
            """
        )

        page.wait_for_timeout(150)

    @staticmethod
    def clear_highlight(locator):
        if not DemoHelper.is_enabled():
            return

        locator.evaluate(
            """
            element => {
                element.style.outline =
                    element.dataset.originalOutline || '';

                element.style.outlineOffset =
                    element.dataset.originalOutlineOffset || '';
            }
            """
        )

    @staticmethod
    def fill_field(page, locator, value):
        if not DemoHelper.is_enabled():
            locator.fill(value)
            return

        DemoHelper.highlight(
            page,
            locator
        )

        locator.fill(value)
        locator.blur()

        expect(locator).to_have_value(value)

        page.wait_for_timeout(80)

        DemoHelper.clear_highlight(
            locator
        )

    @staticmethod
    def hide_demo_overlay(page):
        if not DemoHelper.is_enabled():
            return

        page.evaluate(
            """
            () => {
                const links = [
                    ...document.querySelectorAll('a')
                ];

                const demoLink = links.find(
                    link =>
                        link.href.includes('/admin') ||
                        link.href.includes('/api/v2') ||
                        link.textContent.includes(
                            'Get a live demo'
                        )
                );

                if (!demoLink) {
                    return;
                }

                let element = demoLink;

                while (
                    element &&
                    element !== document.body
                ) {
                    const style =
                        window.getComputedStyle(element);

                    if (
                        style.position === 'fixed' ||
                        style.position === 'sticky'
                    ) {
                        element.style.display = 'none';
                        return;
                    }

                    element = element.parentElement;
                }
            }
            """
        )

    @staticmethod
    def show_result(page, locator):
        if not DemoHelper.is_enabled():
            return

        expect(locator).to_be_visible()

        locator.scroll_into_view_if_needed()

        locator.evaluate(
            """
            element => {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            }
            """
        )

        page.wait_for_timeout(120)

        locator.evaluate(
            """
            element => {
                element.dataset.originalOutline =
                    element.style.outline;

                element.dataset.originalOutlineOffset =
                    element.style.outlineOffset;

                element.style.outline =
                    '4px solid red';

                element.style.outlineOffset =
                    '3px';
            }
            """
        )

        page.wait_for_timeout(300)

        DemoHelper.clear_highlight(locator)

    @staticmethod
    def click(page, locator):
        if not DemoHelper.is_enabled():
            locator.click()
            return

        DemoHelper.highlight(
            page,
            locator
        )

        page.wait_for_timeout(180)

        locator.click()

        page.wait_for_timeout(100)

        try:
            if locator.count() > 0:
                DemoHelper.clear_highlight(
                    locator
                )
        except Exception:
            pass

    @staticmethod
    def check(page, locator):
        if not DemoHelper.is_enabled():
            locator.check()
            return

        DemoHelper.highlight(
            page,
            locator
        )

        locator.check()

        page.wait_for_timeout(120)

        try:
            if locator.count() > 0:
                DemoHelper.clear_highlight(
                    locator
                )
        except Exception:
            pass

    @staticmethod
    def select_option(page, locator, **kwargs):
        if not DemoHelper.is_enabled():
            locator.select_option(**kwargs)
            return

        DemoHelper.highlight(
            page,
            locator
        )

        locator.select_option(
            **kwargs
        )

        page.wait_for_timeout(120)

        try:
            if locator.count() > 0:
                DemoHelper.clear_highlight(
                    locator
                )
        except Exception:
            pass

    @staticmethod
    def show_overlay(page, locator):
        if not DemoHelper.is_enabled():
            return

        locator.scroll_into_view_if_needed()

        locator.evaluate(
            """
            element => {
                const oldOverlay =
                    document.querySelector('#qa-demo-overlay');

                if (oldOverlay) {
                    oldOverlay.remove();
                }

                const rect =
                    element.getBoundingClientRect();

                const overlay =
                    document.createElement('div');

                overlay.id = 'qa-demo-overlay';

                overlay.style.position = 'fixed';
                overlay.style.left = `${rect.left - 5}px`;
                overlay.style.top = `${rect.top - 5}px`;
                overlay.style.width = `${rect.width + 10}px`;
                overlay.style.height = `${rect.height + 10}px`;

                overlay.style.border = '4px solid red';
                overlay.style.borderRadius = '6px';
                overlay.style.boxSizing = 'border-box';

                overlay.style.zIndex = '2147483647';
                overlay.style.pointerEvents = 'none';

                document.body.appendChild(overlay);
            }
            """
        )

    @staticmethod
    def clear_overlay(page):
        if not DemoHelper.is_enabled():
            return

        page.evaluate(
            """
            () => {
                const overlay =
                    document.querySelector('#qa-demo-overlay');

                if (overlay) {
                    overlay.remove();
                }
            }
            """
        )

    @staticmethod
    def add_bottom_space(page):
        if not DemoHelper.is_enabled():
            return

        page.evaluate(
            """
            () => {
                if (document.querySelector('#qa-demo-bottom-space')) {
                    return;
                }

                const spacer = document.createElement('div');

                spacer.id = 'qa-demo-bottom-space';
                spacer.style.height = '300px';
                spacer.style.width = '100%';
                spacer.style.pointerEvents = 'none';

                document.body.appendChild(spacer);
            }
            """
        )