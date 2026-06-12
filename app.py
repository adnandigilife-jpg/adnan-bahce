// app/page.tsx

import { CropCard } from "@/components/CropCard";
import { GrowthChart } from "@/components/GrowthChart";
import { LogForm } from "@/components/LogForm";
import { RecommendationPanel } from "@/components/RecommendationPanel";
import { crops } from "@/lib/data";
import { Camera, CloudSun, Leaf, CalendarDays } from "lucide-react";

export default function HomePage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <section className="mb-8 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="card p-8">
          <p className="mb-3 inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-bold text-green-800">
            Profesyonel bahçe takip paneli
          </p>

          <h1 className="text-4xl font-black tracking-tight md:text-6xl">
            Adnan Bahçe Asistanı
          </h1>

          <p className="mt-4 max-w-2xl text-lg text-slate-600">
            Günlük fotoğraf, sulama, gübre, ilaç, zararlı ve gelişim kayıtlarını
            tek yerde takip et.
          </p>

          <div className="mt-6 grid gap-3 sm:grid-cols-4">
            <Info icon={<Leaf />} title="9 ürün" text="Ayrı takip" />
            <Info icon={<Camera />} title="Fotoğraf" text="Gelişim arşivi" />
            <Info icon={<CloudSun />} title="Hava" text="Sulama kararı" />
            <Info icon={<CalendarDays />} title="Takvim" text="Hatırlatma" />
          </div>
        </div>

        <RecommendationPanel />
      </section>

      <section className="mb-8 grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
        <LogForm />
        <GrowthChart />
      </section>

      <section>
        <h2 className="mb-4 text-2xl font-black">Ürünlerim</h2>

        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {crops.map((crop) => (
            <CropCard key={crop.id} crop={crop} />
          ))}
        </div>
      </section>
    </main>
  );
}

function Info({
  icon,
  title,
  text,
}: {
  icon: React.ReactNode;
  title: string;
  text: string;
}) {
  return (
    <div className="rounded-3xl bg-white/70 p-4">
      <div className="mb-2 h-6 w-6 text-green-700">{icon}</div>
      <b>{title}</b>
      <p className="text-sm text-slate-600">{text}</p>
    </div>
  );
}// lib/data.ts

import { Crop, GardenLog } from "./types";

export const crops: Crop[] = [
  {
    id: "misir",
    name: "Mısır",
    stage: "Boylanma / koçan öncesi",
    healthScore: 91,
    lastWateredDays: 2,
    lastFedDays: 1,
    note: "Amino asit dün uygulandı. Yaprak rengi iyi."
  },

  {
    id: "domates",
    name: "Domates",
    stage: "Çiçek / meyve",
    healthScore: 84,
    lastWateredDays: 2,
    lastFedDays: 6,
    note: "Kalsiyum ve potasyum takibi önemli."
  },

  {
    id: "biber",
    name: "Biber",
    stage: "Çiçek / meyve",
    healthScore: 82,
    lastWateredDays: 2,
    lastFedDays: 6,
    note: "Çiçek dökümü kontrol edilmeli."
  },

  {
    id: "cilek",
    name: "Çilek",
    stage: "Meyve dönemi",
    healthScore: 76,
    lastWateredDays: 2,
    lastFedDays: 7,
    note: "Yaprak altı zararlı kontrolü."
  },

  {
    id: "salatalik",
    name: "Salatalık",
    stage: "Sürgün / meyve",
    healthScore: 79,
    lastWateredDays: 1,
    lastFedDays: 5,
    note: "Külleme riski takip edilmeli."
  },

  {
    id: "kabak",
    name: "Kabak",
    stage: "Çiçeklenme",
    healthScore: 80,
    lastWateredDays: 2,
    lastFedDays: 5,
    note: "Külleme ve meyve bağlama kontrolü."
  },

  {
    id: "bamya",
    name: "Bamya",
    stage: "Gelişim",
    healthScore: 83,
    lastWateredDays: 3,
    lastFedDays: 6,
    note: "Kök bölgesini sürekli ıslak bırakma."
  },

  {
    id: "karpuz",
    name: "Karpuz",
    stage: "Kol atma",
    healthScore: 78,
    lastWateredDays: 3,
    lastFedDays: 7,
    note: "Potasyum ihtiyacı artacak."
  },

  {
    id: "patlican",
    name: "Patlıcan",
    stage: "Çiçek / meyve",
    healthScore: 81,
    lastWateredDays: 2,
    lastFedDays: 6,
    note: "Yaprak biti ve beyaz sinek kontrolü."
  }
];

export const logs: GardenLog[] = [
  {
    id: "1",
    cropId: "misir",
    cropName: "Mısır",
    type: "gubre",
    date: "2026-06-12",
    title: "Amino asit uygulandı",
    note: "Yapraktan amino asit verildi."
  },

  {
    id: "2",
    cropId: "domates",
    cropName: "Domates",
    type: "gozlem",
    date: "2026-06-12",
    title: "Genel kontrol",
    note: "Çiçeklenme devam ediyor."
  }
];

export const growthData = [
  {
    day: "1. Gün",
    misir: 35,
    domates: 22,
    biber: 18,
    patlican: 20
  },

  {
    day: "7. Gün",
    misir: 62,
    domates: 31,
    biber: 25,
    patlican: 29
  },

  {
    day: "14. Gün",
    misir: 95,
    domates: 46,
    biber: 34,
    patlican: 42
  },

  {
    day: "21. Gün",
    misir: 145,
    domates: 61,
    biber: 45,
    patlican: 55
  },

  {
    day: "28. Gün",
    misir: 190,
    domates: 75,
    biber: 55,
    patlican: 68
  }
];// components/CropCard.tsx

import { Droplets, Sprout, Activity } from "lucide-react";

type Crop = {
  id: string;
  name: string;
  stage: string;
  healthScore: number;
  lastWateredDays: number;
  lastFedDays: number;
  note: string;
};

export function CropCard({ crop }: { crop: Crop }) {
  return (
    <div className="rounded-3xl border border-green-100 bg-white p-5 shadow-lg">

      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-green-700">
            Ürün
          </p>

          <h3 className="text-2xl font-bold">
            {crop.name}
          </h3>
        </div>

        <div className="rounded-2xl bg-green-100 px-3 py-2 text-sm font-bold text-green-800">
          %{crop.healthScore}
        </div>
      </div>

      <p className="mt-3 text-sm text-gray-500">
        {crop.stage}
      </p>

      <p className="mt-2 text-sm">
        {crop.note}
      </p>

      <div className="mt-5 grid grid-cols-2 gap-3">

        <div className="rounded-2xl bg-blue-50 p-3">
          <Droplets size={18} />

          <p className="mt-1 text-xs text-gray-500">
            Son Sulama
          </p>

          <p className="font-bold">
            {crop.lastWateredDays} gün önce
          </p>
        </div>

        <div className="rounded-2xl bg-yellow-50 p-3">
          <Sprout size={18} />

          <p className="mt-1 text-xs text-gray-500">
            Son Gübre
          </p>

          <p className="font-bold">
            {crop.lastFedDays} gün önce
          </p>
        </div>

      </div>

      <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-2xl bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700">
        <Activity size={18} />
        Detayları Aç
      </button>

    </div>
  );
}"use client";

import { useState } from "react";

export default function LogForm() {
  const [message, setMessage] = useState("");

  const handleSave = () => {
    setMessage("Kayıt başarıyla kaydedildi.");
  };

  return (
    <div className="rounded-3xl border border-green-100 bg-white p-6 shadow-lg">

      <h2 className="text-2xl font-bold">
        Günlük Bahçe Kaydı
      </h2>

      <p className="mt-1 text-sm text-gray-500">
        Sulama, gübre, ilaç veya gözlem kaydı oluştur.
      </p>

      <div className="mt-5 space-y-4">

        <select className="w-full rounded-2xl border p-3">
          <option>Mısır</option>
          <option>Domates</option>
          <option>Biber</option>
          <option>Çilek</option>
          <option>Salatalık</option>
          <option>Kabak</option>
          <option>Bamya</option>
          <option>Karpuz</option>
          <option>Patlıcan</option>
        </select>

        <select className="w-full rounded-2xl border p-3">
          <option>Sulama</option>
          <option>Gübre</option>
          <option>İlaçlama</option>
          <option>Fotoğraf</option>
          <option>Gözlem</option>
        </select>

        <input
          type="date"
          className="w-full rounded-2xl border p-3"
        />

        <input
          type="text"
          placeholder="Başlık"
          className="w-full rounded-2xl border p-3"
        />

        <textarea
          placeholder="Örn: Dün amino asit uyguladım, yapraklar koyu yeşil."
          className="min-h-[120px] w-full rounded-2xl border p-3"
        />

        <input
          type="file"
          accept="image/*"
          className="w-full rounded-2xl border p-3"
        />

        <button
          onClick={handleSave}
          className="w-full rounded-2xl bg-green-600 py-3 font-semibold text-white hover:bg-green-700"
        >
          Kaydı Kaydet
        </button>

        {message && (
          <div className="rounded-2xl bg-green-100 p-3 text-green-800">
            {message}
          </div>
        )}

      </div>
    </div>
  );
}
