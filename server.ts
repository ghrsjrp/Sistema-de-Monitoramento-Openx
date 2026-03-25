import express from "express";
import cors from "cors";
import path from "path";
import { createServer as createViteServer } from "vite";
import { PrismaClient } from "@prisma/client";
import * as dotenv from "dotenv";

dotenv.config();

const prisma = new PrismaClient();
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// API: Devices
const deviceRouter = express.Router();

deviceRouter.get("/", async (req, res) => {
  try {
    const devices = await prisma.device.findMany({ include: { interfaces: true } });
    res.json(devices);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch devices" });
  }
});

deviceRouter.post("/", async (req, res) => {
  try {
    const { hostname, ipAddress, community, snmpVersion, vendor, model } = req.body;
    const device = await prisma.device.create({
      data: { hostname, ipAddress, community, snmpVersion, vendor, model },
    });
    res.status(201).json(device);
  } catch (error) {
    res.status(400).json({ error: "Failed to create device" });
  }
});

deviceRouter.get("/:id", async (req, res) => {
  try {
    const device = await prisma.device.findUnique({
      where: { id: req.params.id },
      include: { interfaces: true },
    });
    if (!device) return res.status(404).json({ error: "Device not found" });
    res.json(device);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch device" });
  }
});

// API: Interfaces
const interfaceRouter = express.Router();

interfaceRouter.get("/device/:deviceId", async (req, res) => {
  try {
    const interfaces = await prisma.interface.findMany({
      where: { deviceId: req.params.deviceId },
    });
    res.json(interfaces);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch interfaces" });
  }
});

// Register Routers
app.use("/api/devices", deviceRouter);
app.use("/api/interfaces", interfaceRouter);

// Vite middleware for development
async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Openx Monitoring Server running on http://localhost:${PORT}`);
  });
}

startServer();
