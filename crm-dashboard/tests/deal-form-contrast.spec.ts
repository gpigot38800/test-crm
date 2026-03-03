import { test, expect } from '@playwright/test';

test.describe('Formulaire Deal - Contraste et lisibilité', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('le bouton Nouveau Deal est visible et ouvre le modal', async ({ page }) => {
    const btn = page.locator('#btn-new-deal');
    await expect(btn).toBeVisible();
    await btn.click();
    const modal = page.locator('#deal-modal');
    await expect(modal).toBeVisible();
    await page.screenshot({ path: 'tests/screenshots/modal-open.png' });
  });

  test('les labels du formulaire ont un bon contraste sur fond sombre', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    const labels = page.locator('#deal-form label');
    const count = await labels.count();
    expect(count).toBeGreaterThanOrEqual(5);

    for (let i = 0; i < count; i++) {
      const label = labels.nth(i);
      const color = await label.evaluate(el => getComputedStyle(el).color);
      // #cbd5e1 = rgb(203, 213, 225) — texte clair, bien lisible
      expect(color).not.toBe('rgb(55, 65, 81)'); // text-gray-700 = trop sombre
      expect(color).not.toBe('rgb(75, 85, 99)');  // text-gray-600
    }
  });

  test('les champs de saisie ont un texte clair lisible', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    // Remplir le champ client
    const clientInput = page.locator('#deal-client');
    await clientInput.fill('Test Entreprise');

    const textColor = await clientInput.evaluate(el => getComputedStyle(el).color);
    // Le texte doit être clair (proche de blanc)
    const match = textColor.match(/rgb\((\d+), (\d+), (\d+)\)/);
    expect(match).not.toBeNull();
    if (match) {
      const [, r, g, b] = match.map(Number);
      // Les valeurs RGB doivent être > 180 pour être lisible sur fond sombre
      expect(r).toBeGreaterThan(180);
      expect(g).toBeGreaterThan(180);
      expect(b).toBeGreaterThan(180);
    }

    await page.screenshot({ path: 'tests/screenshots/form-filled-client.png' });
  });

  test('le champ montant (number) a un texte lisible', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    const montantInput = page.locator('#deal-montant');
    await montantInput.fill('25000');

    const textColor = await montantInput.evaluate(el => getComputedStyle(el).color);
    const match = textColor.match(/rgb\((\d+), (\d+), (\d+)\)/);
    expect(match).not.toBeNull();
    if (match) {
      const [, r, g, b] = match.map(Number);
      expect(r).toBeGreaterThan(180);
      expect(g).toBeGreaterThan(180);
      expect(b).toBeGreaterThan(180);
    }

    await page.screenshot({ path: 'tests/screenshots/form-filled-montant.png' });
  });

  test('le textarea (notes) a un texte lisible', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    const notes = page.locator('#deal-notes');
    await notes.fill('Notes de test pour vérifier le contraste');

    const textColor = await notes.evaluate(el => getComputedStyle(el).color);
    const match = textColor.match(/rgb\((\d+), (\d+), (\d+)\)/);
    expect(match).not.toBeNull();
    if (match) {
      const [, r, g, b] = match.map(Number);
      expect(r).toBeGreaterThan(180);
      expect(g).toBeGreaterThan(180);
      expect(b).toBeGreaterThan(180);
    }
  });

  test('le fond du modal a un contraste correct', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    const modalContent = page.locator('.modal-content');
    const bgColor = await modalContent.evaluate(el => getComputedStyle(el).backgroundColor);

    // Le fond doit être sombre (var(--bg-secondary) = #1e293b = rgb(30, 41, 59))
    const match = bgColor.match(/rgb\((\d+), (\d+), (\d+)\)/);
    expect(match).not.toBeNull();
    if (match) {
      const [, r, g, b] = match.map(Number);
      // Valeurs sombres attendues (< 100)
      expect(r).toBeLessThan(100);
      expect(g).toBeLessThan(100);
      expect(b).toBeLessThan(100);
    }
  });

  test('les champs ont une bordure visible', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    const clientInput = page.locator('#deal-client');
    const borderColor = await clientInput.evaluate(el => getComputedStyle(el).borderColor);

    // La bordure ne doit pas être transparente ou invisible
    expect(borderColor).not.toBe('rgb(0, 0, 0)');
    expect(borderColor).not.toBe('transparent');
  });

  test('le formulaire complet rempli est lisible - screenshot', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    // Remplir tous les champs
    await page.locator('#deal-client').fill('Acme Corporation');
    await page.locator('#deal-statut').selectOption('Négociation');
    await page.locator('#deal-montant').fill('75000');
    await page.locator('#deal-secteur').fill('Tech / SaaS');
    await page.locator('#deal-echeance').fill('2026-04-15');
    await page.locator('#deal-assignee').fill('Jean Dupont');
    await page.locator('#deal-notes').fill('Deal stratégique - grande entreprise avec potentiel de croissance important.');

    await page.screenshot({ path: 'tests/screenshots/form-complete.png', fullPage: false });
  });

  test('les boutons Annuler et Enregistrer sont visibles', async ({ page }) => {
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    const cancelBtn = page.locator('#btn-modal-cancel');
    const saveBtn = page.locator('#btn-modal-save');

    await expect(cancelBtn).toBeVisible();
    await expect(saveBtn).toBeVisible();

    // Vérifier que le bouton Enregistrer a un fond coloré (cyan)
    const saveBg = await saveBtn.evaluate(el => getComputedStyle(el).backgroundColor);
    expect(saveBg).not.toBe('rgba(0, 0, 0, 0)');
    expect(saveBg).not.toBe('transparent');
  });

  test('responsive mobile - le modal est accessible', async ({ page, browserName }, testInfo) => {
    if (testInfo.project.name !== 'mobile') {
      test.skip();
    }
    await page.locator('#btn-new-deal').click();
    await expect(page.locator('#deal-modal')).toBeVisible();

    const modal = page.locator('.modal-content');
    const box = await modal.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      // Le modal ne doit pas dépasser la largeur de l'écran mobile
      expect(box.width).toBeLessThanOrEqual(375);
    }

    await page.screenshot({ path: 'tests/screenshots/form-mobile.png' });
  });
});
