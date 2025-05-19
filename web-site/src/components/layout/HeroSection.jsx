
import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';

const HeroSection = () => {
  const handleGetInTouchClick = () => {
    const contactSection = document.querySelector('#contact');
    if (contactSection) {
      contactSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative py-20 md:py-32 bg-gradient-to-r from-indigo-600 to-sky-500 text-white overflow-hidden">
      <div className="absolute inset-0 opacity-20">
         <img  
            className="w-full h-full object-cover" 
            alt="Abstract network background"
           src="https://images.unsplash.com/photo-1585753035830-8205de3dd213" />
      </div>
      <div className="container mx-auto px-4 relative z-10 text-center">
        <motion.h1 
          className="text-4xl sm:text-5xl md:text-6xl font-extrabold mb-6 leading-tight"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: "easeOut" }}
        >
          Revolutionizing AI Content Management
        </motion.h1>
        <motion.p 
          className="text-lg sm:text-xl md:text-2xl mb-10 max-w-3xl mx-auto text-indigo-100"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2, ease: "easeOut" }}
        >
          LangGraphSemantic offers an enterprise-grade solution for storing, securing, and searching AI-generated data.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.4, ease: "easeOut" }}
        >
          <Button 
            size="lg" 
            className="bg-white text-indigo-600 hover:bg-indigo-50 font-semibold shadow-lg transform hover:scale-105 transition-transform duration-300"
            onClick={handleGetInTouchClick}
          >
            Get in Touch
          </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
  