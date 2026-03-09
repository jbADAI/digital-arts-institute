// Proxies file upload to AssemblyAI. Keys stay server-side.
export const config = { api: { bodyParser: { sizeLimit: '100mb' } } };

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const key = process.env.ASSEMBLYAI_API_KEY;
  if (!key) return res.status(500).json({ error: "ASSEMBLYAI_API_KEY not configured" });

  try {
    const response = await fetch("https://api.assemblyai.com/v2/upload", {
      method: "POST",
      headers: { authorization: key, "content-type": "application/octet-stream" },
      body: req.body,
    });
    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
