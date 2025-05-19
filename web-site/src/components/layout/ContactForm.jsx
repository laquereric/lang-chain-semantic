import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { supabase } from '@/lib/supabaseClient';

const ContactForm = () => {
  const { toast } = useToast();
  const qrCodeUrl = "https://storage.googleapis.com/hostinger-horizons-assets-prod/5139d417-c972-44ee-b188-1397963c2935/64be9fcbd1d810f793a351a2e4762da8.png";

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');

    try {
      const { data, error } = await supabase
        .from('contacts') 
        .insert([{ name, email, message }]);

      if (error) {
        throw error;
      }

      toast({
        title: "Message Sent!",
        description: "Thank you for reaching out. We'll be in touch soon.",
        variant: "default",
      });
      e.target.reset();
    } catch (error) {
      console.error('Error submitting contact form:', error);
      toast({
        title: "Error Sending Message",
        description: "There was a problem submitting your message. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <motion.section 
      id="contact" 
      className="py-16 sm:py-24 bg-slate-800 text-white"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.8 }}
    >
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4 text-sky-400">Get In Touch</h2>
          <p className="text-lg text-slate-300">
            Interested in learning more or partnering with us? We'd love to hear from you. Fill out the form or scan the QR code.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-12 items-start">
          <motion.form 
            className="bg-slate-700 p-8 rounded-xl shadow-2xl"
            onSubmit={handleContactSubmit}
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-slate-300">Full Name</label>
                <input type="text" name="name" id="name" required className="mt-1 block w-full px-4 py-2.5 bg-slate-600 border border-slate-500 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 text-white placeholder-slate-400" placeholder="Your Name" />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-300">Email Address</label>
                <input type="email" name="email" id="email" required className="mt-1 block w-full px-4 py-2.5 bg-slate-600 border border-slate-500 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 text-white placeholder-slate-400" placeholder="you@example.com" />
              </div>
              <div>
                <label htmlFor="message" className="block text-sm font-medium text-slate-300">Message</label>
                <textarea name="message" id="message" rows="4" required className="mt-1 block w-full px-4 py-2.5 bg-slate-600 border border-slate-500 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 text-white placeholder-slate-400" placeholder="Your message..."></textarea>
              </div>
              <div>
                <Button type="submit" className="w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3">
                  Send Message
                </Button>
              </div>
            </div>
          </motion.form>

          <motion.div 
            className="flex flex-col items-center bg-slate-700 p-8 rounded-xl shadow-2xl"
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <h3 className="text-xl font-semibold text-sky-400 mb-4">Scan to Connect</h3>
            <div className="bg-white p-4 rounded-lg shadow-md">
              <img src={qrCodeUrl} alt="Contact QR Code" className="w-48 h-48 md:w-56 md:h-56 object-contain" />
            </div>
            <p className="text-slate-300 mt-4 text-center text-sm">
              Scan this QR code with your device to quickly get our contact information or visit our website.
            </p>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
};

export default ContactForm;
