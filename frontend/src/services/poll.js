export function pollUntil(fetchStatus, isDone, { intervalMs = 1500, timeoutMs = 60000 } = {}) {
  const start = Date.now();

  return new Promise((resolve, reject) => {
    const tick = async () => {
      try {
        const data = await fetchStatus();

        if (isDone(data)) {
          resolve(data);
          return;
        }

        if (Date.now() - start > timeoutMs) {
          reject(new Error("Timed out waiting for processing to complete"));
          return;
        }

        setTimeout(tick, intervalMs);
      } catch (err) {
        reject(err);
      }
    };

    tick();
  });
}
