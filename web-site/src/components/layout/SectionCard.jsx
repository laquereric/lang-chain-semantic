
import React from 'react';
import { motion } from 'framer-motion';

const SectionCard = ({ title, subtitle, points, imagePlaceholder, imageBgColor, id, index, imgSrc }) => {
  const isEven = index % 2 === 0;
  return (
    <motion.section
      id={id}
      className="py-16 sm:py-24 overflow-hidden"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.6 }}
    >
      <div className="container mx-auto px-4">
        <div className={`flex flex-col ${isEven ? 'md:flex-row' : 'md:flex-row-reverse'} items-center gap-8 md:gap-12`}>
          <div className="md:w-1/2">
            <motion.h2 
              className="text-3xl sm:text-4xl font-bold text-slate-800 mb-3"
              initial={{ opacity: 0, x: isEven ? -50 : 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              {title}
            </motion.h2>
            <motion.p 
              className="text-lg text-slate-600 mb-6"
              initial={{ opacity: 0, x: isEven ? -50 : 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              {subtitle}
            </motion.p>
            <ul className="space-y-3">
              {points.map((point, i) => (
                <motion.li
                  key={i}
                  className="flex items-start text-slate-700"
                  initial={{ opacity: 0, x: isEven ? -50 : 50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, amount: 0.5 }}
                  transition={{ duration: 0.5, delay: 0.4 + i * 0.1 }}
                >
                  <svg className="w-5 h-5 text-indigo-500 mr-2 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                  </svg>
                  <span>{point}</span>
                </motion.li>
              ))}
            </ul>
          </div>
          <motion.div 
            className="md:w-1/2 mt-8 md:mt-0"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true, amount: 0.5 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className={`rounded-xl shadow-2xl overflow-hidden p-2 ${imageBgColor}`}>
              <div className="aspect-w-4 aspect-h-3">
                 <img  
                    className="object-cover w-full h-full rounded-lg" 
                    alt={imagePlaceholder}
                   src={imgSrc || "https://images.unsplash.com/photo-1675023112817-52b789fd2ef0"} />
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
};

export default SectionCard;
  