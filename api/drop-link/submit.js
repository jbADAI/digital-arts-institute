// Receives a URL signal from the drop-link form and writes it to GitHub inbox/.
export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const token = process.env.GITHUB_TOKEN;
  const repo = process.env.GITHUB_REPO || "jbADAI/digital-arts-institute";
  if (!token) return res.status(500).json({ error: "GITHUB_TOKEN not configured" });

  const { url, note, submitted_by, _hp } = req.body;

  // Honeypot check
  if (_hp) return res.status(200).json({ ok: true, title: "received" });

  if (!url) return res.status(400).json({ error: "URL is required" });

  try {
    // Build slug from URL
    const urlObj = new URL(url);
    const slug = (urlObj.hostname + urlObj.pathname)
      .replace(/^www\./, "")
      .replace(/[^a-z0-9]+/gi, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60)
      .toLowerCase();

    const today = new Date().toISOString().split("T")[0];
    const inboxFilename = `${today}-${slug}.md`;
    const nodeId = `signal-${today}-${slug}`;
    const contributor = submitted_by || "community";

    const content = `---
id: ${nodeId}
date_captured: ${today}
source_type: link
submitted_by: ${contributor}
protocol_stage: SENSE
status: raw
signal_type: link
url: ${url}
provenance: community
confidence: unverified
---

## Source

${url}

${note ? `## Contributor Note\n\n${note}\n` : ""}
`;

    const encoded = Buffer.from(content, "utf-8").toString("base64");
    const apiUrl = `https://api.github.com/repos/${repo}/contents/inbox/${inboxFilename}`;

    const response = await fetch(apiUrl, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      body: JSON.stringify({
        message: `signal: drop-link ${inboxFilename}`,
        content: encoded,
      }),
    });

    if (!response.ok) {
      const err = await response.json();
      return res.status(response.status).json({ error: err.message || "GitHub API error" });
    }

    // Extract a title from the URL for the success message
    const title = urlObj.hostname.replace(/^www\./, "") + urlObj.pathname.replace(/\/$/, "");

    return res.status(200).json({ ok: true, title });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
