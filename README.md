---
title: "Trabalho de Implementação 2 - Gerador e Verificador de Assinaturas Digitais RSA"
author: "H. de M. O. Lima – 211055281, L. P. Torres – 222011623, and M. N. Miyata – 180126890"
abstract: "Este trabalho apresenta a implementação de um gerador e verificador de assinaturas digitais utilizando o algoritmo RSA. O objetivo é garantir a autenticidade e integridade das mensagens trocadas entre as partes envolvidas. A implementação inclui a geração de chaves públicas e privadas, a assinatura digital de mensagens e a verificação dessas assinaturas. O trabalho também discute os desafios enfrentados durante o desenvolvimento e as soluções adotadas para superá-los."
keywords:
  [
    "Assinaturas Digitais",
    "RSA",
    "Criptografia",
  ]
bibliography: [ "references.bib" ]
---

# Introdução

O RSA (Rivest-Shamir-Adleman) é um algoritmo de criptografia assimétrica, em que são utilizadas duas chaves distintas:
uma chave pública para criptografar mensagens e uma chave privada para descriptografá-las. O surgimento do RSA foi
importante para resolver o problema de enviar uma mensagem criptografada sem que o remetente e o destinatário precisem
compartilhar uma chave secreta previamente.

O presente trabalho foi implementado em três partes: (1) geração de chaves públicas e privadas, (2) assinatura digital
de
mensagens e (3) verificação de assinaturas digitais e descriptografia de mensagens. A seguir, cada uma dessas partes é
discutida em detalhes.

# Geração de Chaves