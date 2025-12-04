import asyncio
from playwright.async_api import async_playwright

STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

window.chrome = { runtime: {} };

Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
});

Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en']
});

const originalQuery = navigator.permissions.query;
navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters)
);

const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(param) {
    if (param === 37445) return 'Intel Open Source Technology Center';
    if (param === 37446) return 'Mesa DRI Intel(R) Ivybridge Mobile ';
    return getParameter.call(this, param);
};
"""

async def run():
    async with async_playwright() as p:

        # ⭐ Launch NORMAL Chrome (not persistent)
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            ignore_default_args=[
                "--enable-automation",
                "--disable-blink-features=AutomationControlled",
                "--remote-debugging-pipe",
            ],
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
            ]
        )

        # ⭐ Create a new clean page (NO FREEZE)
        page = await browser.new_page()

        # ⭐ Inject stealth BEFORE page loads
        await page.add_init_script(STEALTH_JS)

        print("Opening login page...")
        await page.goto(
            "https://popularenlinea.com/empresarial/paginas/servicios/ib-empresarial.aspx",
            wait_until="domcontentloaded"
        )

        print("Clicking ACCEDER button...")
        await page.click("#btn_bpd_login")
        await asyncio.sleep(2)

        print("Typing credentials...")
        await page.type("input.nombre_empresa", "andalerd", delay=120)
        await page.type("input.usuario_empresa", "andaleumbra", delay=120)
        await page.type("input.pass_empresa", "Umbra1010.", delay=120)
        await asyncio.sleep(2)

        print("Clicking login button...")
        await page.click("button.acceder_empresa")

        print("Waiting for dashboard load...")
        await page.wait_for_timeout(8000)

        print("Expanding Banco menu...")
        await page.click("button[data-testid='Banco']")
        await asyncio.sleep(2)

        print("Clicking Cuentas submenu...")
        await page.click("button[data-testid='sidemenu-Cuentas']")

        print("Done — waiting 60 sec for inspection...")
        await asyncio.sleep(60000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
