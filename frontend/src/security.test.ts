test('security regression placeholder is explicit', () => { expect(import.meta.env.VITE_GOOGLE_API_KEY).toBeUndefined(); });
