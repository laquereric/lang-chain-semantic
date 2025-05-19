
import React from 'react';
import { Toaster } from '@/components/ui/toaster';
import Header from '@/components/layout/Header';
import HeroSection from '@/components/layout/HeroSection';
import SectionCard from '@/components/layout/SectionCard';
import ContactForm from '@/components/layout/ContactForm';
import Footer from '@/components/layout/Footer';
import { sectionsData } from '@/data/siteData';

const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-sky-100 text-slate-900 font-sans">
      <Header />
      <main>
        <HeroSection />
        {sectionsData.map((section, index) => (
          <SectionCard 
            key={section.id}
            id={section.id}
            title={section.title}
            subtitle={section.subtitle}
            points={section.points}
            imagePlaceholder={section.imagePlaceholder}
            imageBgColor={section.imageBgColor}
            imgSrc={section.imgSrc}
            index={index}
          />
        ))}
        <ContactForm />
      </main>
      <Footer />
      <Toaster />
    </div>
  );
};

export default App;
  