// Writes a signal markdown file to GitHub inbox/. Key stays server-side.
export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const token = process.env.GITHUB_TOKEN;
  const repo = process.env.GITHUB_REPO || "jbADAI/digital-arts-institute";
  if (!token) return res.status(500).json({ error: "GITHUB_TOKEN not configured" });

  const { filename, content } = req.body;
  if (!filename || !content) return res.status(400).json({ error: "Missing filename or content" });

  try {
    const encoded = Buffer.from(content, "utf-8").toString("base64");
    const apiUrl = `https://api.github.com/repos/${repo}/contents/inbox/${filename}`;

    const response = await fetch(apiUrl, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      body: JSON.stringify({
        message: `signal: transcribe ${filename}`,
        content: encoded,
      }),
    });

    const data = await response.json();
    if (!response.ok) return res.status(response.status).json(data);

    return res.status(200).json({
      html_url: data.content?.html_url ?? `https://github.com/${repo}/blob/main/inbox/${filename}`,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
