import os
import urllib
import random
import asyncio
import requests
from telegraph import upload_file
from pyrogram import Client, filters

from Stark.db import DB
from Stark import error_handler

kakashitext = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]

AVATARS = [
     "https://telegra.ph//file/77c17cea26e8c24c36ea8.jpg",
     "https://telegra.ph//file/e7f88921671418be96686.jpg",
     "https://telegra.ph//file/10371646861fcfb521195.jpg",
     "https://telegra.ph//file/1ab533ec778f56c4ecc5f.jpg",
     "https://telegra.ph//file/75b0d1a20e8e9283c067b.jpg",
     "https://telegra.ph//file/7939490055915bed0585c.jpg",
     "https://telegra.ph//file/cd6dd4acae3c276c065be.jpg",
     "https://telegra.ph//file/fced18b5d48c0cc3abb46.jpg",
     "https://telegra.ph//file/79f1ccebc6aba285c6038.jpg",
     "https://telegra.ph//file/a3423cefc893a6cd6032d.jpg",
     "https://telegra.ph//file/2cc12ce620a035510b71d.jpg",
     "https://telegra.ph//file/f40ec98eb82f48e301480.jpg",
     "https://telegra.ph//file/e14a9c34b0bd6dab04333.jpg",
     "https://telegra.ph//file/d782da8113a71bbd6e64c.jpg",
     "https://telegra.ph//file/e3d4ac98f08cc3e1a5c74.jpg",
     "https://telegra.ph//file/f5fe3e20d9ff18edf2cde.jpg",
     "https://telegra.ph//file/156fb0e4fb7b16e1ad53f.jpg",
     "https://telegra.ph//file/46997187cdadd13af1a4a.jpg",
     "https://telegra.ph//file/e4484c6f3aafb531881fe.jpg",
     "https://telegra.ph//file/8706beb96352012a02225.jpg",
     "https://telegra.ph//file/42af4f48fa7684cd9709e.jpg",
     "https://telegra.ph//file/b835311fae7dfbcb5a110.jpg",
     "https://telegra.ph//file/13e782d79a69df17256ac.jpg",
     "https://telegra.ph//file/556d9f06cedd634dc6e0b.jpg",
     "https://telegra.ph//file/63b7803170528445cd2ea.jpg",
     "https://telegra.ph//file/19364431c410895b30666.jpg",
     "https://telegra.ph//file/02a9eec0c7d58a9a2d2da.jpg",
     "https://telegra.ph//file/99c47bba3528fb3513bf7.jpg",
     "https://telegra.ph//file/04b8c4fdcecc4f08a0337.jpg",
     "https://telegra.ph//file/56fc54bdb387b21508dc4.jpg",
     "https://telegra.ph//file/06f01066e22923b3fa07c.jpg",
     "https://telegra.ph//file/3be8c6038f938679b287a.jpg",
     "https://telegra.ph//file/c84d1903f515c2bd9a5a5.jpg",
     "https://telegra.ph//file/f73ab4cb251dd5a1faeb6.jpg",
     "https://telegra.ph//file/199fb4dfabb5a966e2cc5.png",
     "https://telegra.ph//file/6c154cf21a9debdeb0f10.jpg",
     "https://telegra.ph//file/199fb4dfabb5a966e2cc5.png",
     "https://telegra.ph//file/9173ece9ac42e18bca59f.jpg",
     "https://telegra.ph//file/34f4d70b52785b6c7d519.jpg",
     "https://telegra.ph//file/9d197b2720c58bd7635d6.png",
     "https://telegra.ph//file/cd793eb6485c251acb821.png",
     "https://telegra.ph//file/bdf9039fd7adcf74c64ea.png",
     "https://telegra.ph//file/b9770ec62a54fefd466b2.jpg",
 ]
kakashiemoji = [
    "⁭\n                    💖\n                  💖💖\n               💖💖💖\n            💖💖 💖💖\n          💖💖    💖💖\n        💖💖       💖💖\n      💖💖💖💖💖💖\n     💖💖💖💖💖💖💖\n   💖💖                 💖💖\n  💖💖                    💖💖\n💖💖                       💖💖\n",
    "⁭\n💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗💗\n💗💗                     💗💗\n💗💗                     💗💗\n💗💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗💗\n💗💗                     💗💖\n💗💗                     💗💖\n💗💗💗💖💗💗💗💗\n💗💗💗💗💗💗💗\n",
    "⁭\n          💛💛💛💛💛💛\n     💛💛💛💛💛💛💛💛\n   💛💛                      💛💛\n 💛💛\n💛💛\n💛💛\n {💛💛}\n   💛💛                      💛💛\n     💛💛💛💛💛💛💛💛\n         💛💛💛💛💛💛\n",
    "⁭\n💙💙💙💙💙💙💙\n💙💙💙💙💙💙💙💙\n💙💙                      💙💙\n💙💙                         💙💙\n💙💙                         💙💙\n💙💙                         💙💙\n💙💙                         💙💙\n💙💙                      💙💙\n💙💙💙💙💙💙💙💙\n💙💙💙💙💙💙💙\n",
    "⁭\n💟💟💟💟💟💟💟💟\n💟💟💟💟💟💟💟💟\n💟💟\n💟💟\n💟💟💟💟💟💟\n💟💟💟💟💟💟\n💟💟\n💟💟\n💟💟💟💟💟💟💟💟\n💟💟💟💟💟💟💟💟\n",
    "⁭\n💚💚💚💚💚💚💚💚\n💚💚💚💚💚💚💚💚\n💚💚\n💚💚\n💚💚💚💚💚💚\n💚💚💚💚💚💚\n💚💚\n💚💚\n💚💚\n💚💚\n",
    "⁭\n          💜💜💜💜💜💜\n     💜💜💜💜💜💜💜💜\n   💜💜                     💜💜\n 💜💜\n💜💜                💜💜💜💜\n💜💜                💜💜💜💜\n 💜💜                        💜💜\n   💜💜                      💜💜\n     💜💜💜💜💜💜💜💜\n          💜💜💜💜💜💜💜💜\n",
    "⁭\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖💖💖💖💖💖💖💖💖\n💖💖💖💖💖💖💖💖💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n",
    "⁭\n💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗💗\n💗💗\n💗💗\n💗💗💗💗💗💗\n💗💗💗💗💗💗\n💗💗\n💗💗\n💗💗\n💗💗\n",
    "⁭\n        💙💙💙💙\n   💙💙💙💙💙💙\n💙💙               💙💙\n💙💙               💙💙\n   💙💙💙💙💙💙\n   💙💙💙💙💙💙\n💙💙               💙💙\n💙💙               💙💙\n   💙💙💙💙💙💙\n        💙💙💙💙\n",
    "⁭\n        💟💟💟💟\n   💟💟💟💟💟💟\n💟💟               💟💟\n💟💟               💟💟\n 💟💟💟💟💟💟💟\n      💟💟💟💟💟💟💟💟\n                         💟💟\n                        💟💟\n  💟💟💟💟💟💟\n       💟💟💟💟\n",
]


itachiemoji = [
    "⁭\n                    {cj}\n                  {cj}{cj}\n               {cj}{cj}{cj}\n            {cj}{cj} {cj}{cj}\n          {cj}{cj}    {cj}{cj}\n        {cj}{cj}       {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                 {cj}{cj}\n  {cj}{cj}                    {cj}{cj}\n{cj}{cj}                       {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n          {cj}{cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                      {cj}{cj}\n {cj}{cj}\n{cj}{cj}\n{cj}{cj}\n {cj}{cj}\n   {cj}{cj}                      {cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}\n         {cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n          {cj}{cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n {cj}{cj}\n{cj}{cj}                {cj}{cj}{cj}{cj}\n{cj}{cj}                {cj}{cj}{cj}{cj}\n {cj}{cj}                        {cj}{cj}\n   {cj}{cj}                      {cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n          {cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n         {cj}{cj}{cj}{cj}{cj}{cj}\n         {cj}{cj}{cj}{cj}{cj}{cj}\n                  {cj}{cj}\n                  {cj}{cj}\n                  {cj}{cj}\n                  {cj}{cj}\n{cj}{cj}          {cj}{cj}\n  {cj}{cj}       {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                  {cj}{cj}\n{cj}{cj}             {cj}{cj}\n{cj}{cj}        {cj}{cj}\n{cj}{cj}   {cj}{cj}\n{cj}{cj}{cj}{cj}\n{cj}{cj} {cj}{cj}\n{cj}{cj}     {cj}{cj}\n{cj}{cj}         {cj}{cj}\n{cj}{cj}              {cj}{cj}\n{cj}{cj}                   {cj}{cj}\n",
    "⁭\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}{cj}                      {cj}{cj}{cj}\n{cj}{cj}{cj}{cj}            {cj}{cj}{cj}{cj}\n{cj}{cj}    {cj}{cj}    {cj}{cj}    {cj}{cj}\n{cj}{cj}        {cj}{cj}{cj}        {cj}{cj}\n{cj}{cj}             {cj}             {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n",
    "⁭\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}{cj}                       {cj}{cj}\n{cj}{cj}{cj}{cj}                 {cj}{cj}\n{cj}{cj}  {cj}{cj}               {cj}{cj}\n{cj}{cj}     {cj}{cj}            {cj}{cj}\n{cj}{cj}         {cj}{cj}        {cj}{cj}\n{cj}{cj}             {cj}{cj}    {cj}{cj}\n{cj}{cj}                 {cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}{cj}\n{cj}{cj}                          {cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n {cj}{cj}                       {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n {cj}{cj}                       {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n            {cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}    {cj}{cj}\n{cj}{cj}         {cj}{cj}\n{cj}{cj}              {cj}{cj}\n{cj}{cj}                  {cj}{cj}\n",
    "⁭\n       {cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}                 {cj}{cj}\n{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n                            {cj}{cj}\n{cj}{cj}                 {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n       {cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n",
    "⁭\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n  {cj}{cj}                  {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n            {cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                              {cj}{cj}\n  {cj}{cj}                          {cj}{cj}\n    {cj}{cj}                      {cj}{cj}\n      {cj}{cj}                  {cj}{cj}\n         {cj}{cj}              {cj}{cj}\n           {cj}{cj}         {cj}{cj}\n             {cj}{cj}     {cj}{cj}\n               {cj}{cj} {cj}{cj}\n                  {cj}{cj}{cj}\n                       {cj}\n",
    "⁭\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}              {cj}            {cj}{cj}\n {cj}{cj}           {cj}{cj}          {cj}{cj}\n {cj}{cj}        {cj}{cj}{cj}       {cj}{cj}\n  {cj}{cj}   {cj}{cj}  {cj}{cj}   {cj}{cj}\n   {cj}{cj}{cj}{cj}      {cj}{cj}{cj}{cj}\n    {cj}{cj}{cj}             {cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                    {cj}{cj}\n   {cj}{cj}              {cj}{cj}\n      {cj}{cj}        {cj}{cj}\n         {cj}{cj}  {cj}{cj}\n            {cj}{cj}{cj}\n            {cj}{cj}{cj}\n         {cj}{cj} {cj}{cj}\n      {cj}{cj}       {cj}{cj}\n   {cj}{cj}             {cj}{cj}\n{cj}{cj}                   {cj}{cj}\n",
    "⁭\n{cj}{cj}                    {cj}{cj}\n   {cj}{cj}              {cj}{cj}\n      {cj}{cj}        {cj}{cj}\n         {cj}{cj}  {cj}{cj}\n            {cj}{cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n",
    "⁭\n {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n                       {cj}{cj}\n                   {cj}{cj}\n               {cj}{cj}\n           {cj}{cj}\n       {cj}{cj}\n   {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n       {cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n        {cj}{cj}{cj}{cj}\n",
    "⁭\n          {cj}{cj}\n     {cj}{cj}{cj}\n{cj}{cj} {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n     {cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}\n",
    "⁭\n    {cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}          {cj}{cj}\n                {cj}{cj}\n             {cj}{cj}\n          {cj}{cj}\n       {cj}{cj}\n    {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n     {cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}\n{cj}{cj}         {cj}{cj}\n                   {cj}{cj}\n            {cj}{cj}{cj}\n            {cj}{cj}{cj}\n                   {cj}{cj}\n{cj}{cj}         {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}\n",
    "⁭\n                         {cj}{cj}\n                    {cj}{cj}{cj}\n              {cj}{cj} {cj}{cj}\n          {cj}{cj}     {cj}{cj}\n     {cj}{cj}          {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n                         {cj}{cj}\n                         {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n {cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}\n                    {cj}{cj}\n                    {cj}{cj}\n{cj}{cj}          {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}\n",
    "⁭\n        {cj}{cj}{cj}{cj}\n    {cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n    {cj}{cj}{cj}{cj}{cj}{cj}\n        {cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n                      {cj}{cj}\n                     {cj}{cj}\n                   {cj}{cj}\n                 {cj}{cj}\n               {cj}{cj}\n             {cj}{cj}\n           {cj}{cj}\n         {cj}{cj}\n",
    "⁭\n        {cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n        {cj}{cj}{cj}{cj}\n",
    "⁭\n        {cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n                         {cj}{cj}\n                        {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n       {cj}{cj}{cj}{cj}\n",
]


normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]
# List of sad quotes # Because there should be a list to get random.
sad_quotes = [
    "The worst kind of sad is not being able to explain why.",
    "Tears are words that need to be written.",
    "Behind every beautiful thing, there's been some kind of pain.",
    "It's hard to forget someone who gave you so much to remember.",
    "The only thing more shocking than the truth are the lies people tell to cover it up.",
    "It hurts when you have someone in your heart but not in your arms.",
    "Sometimes you have to know when to give up and walk away, but it hurts like hell.",
    "The longer and more carefully we look at a funny story, the sadder it becomes.",
    "You cannot protect yourself from sadness without protecting yourself from happiness.",
    "I am not happy without you in my life, and I will never be happy again.",
      "Programming is like a puzzle. You try every possible combination until the code fits, but sometimes the pieces just won't come together.",
    "The saddest part of programming is when you realize your code is not working and you don't know why.",
    "The worst kind of bug is the one you can't reproduce.",
    "Debugging is like being a detective in a crime movie where you are also the murderer.",
    "The best code is the one never written, but the worst is the one written and never tested.",
    "The code may be elegant, but if it doesn't work, it's just a pretty mess.",
    "Programming is like walking a tightrope. One mistake and you're back to square one.",
    "The code you write is only as good as the testing you put it through.",
    "The hardest part of programming is not the coding, but the debugging.",
    "Programming is like a never-ending game of whack-a-mole. You fix one bug and another one pops up.",
]
#Call client to say cmd, otherwise it wont listen --Unknown
    #idk why i made this function instead of directly using random in message
def sed_gen(sad_quotes):
	qt = random.choice(sad_quotes)
	return qt 
	
@Client.on_message(filters.command(["sed", "sad"]))
@error_handler
async def sed_qoute(c, m):
	qt = sed_gen(sad_quotes)
	if not m.reply_to_message:
		await m.reply_text(qt)
		return
	if m.reply_to_message:
		await c.send_message(m.chat.id, qt, reply_to_message_id=m.reply_to_message.id)
		return

#Code finished ntg to see now...
# qt = DB.qt

# async def add_qt(chat_id):
#     stark = qt.find_one({"chat_id": chat_id})
#     if stark is None:
#         qt.insert_one({"chat_id": chat_id})


# async def del_qt(chat_id):
#     qt.delete_one({"chat_id": chat_id})


# @Client.on_message(filters.command(["add_qt"]))
# @error_handler
# async def qt_add(c, m):
# 	x = await m.reply_text("__Adding Chat to DataBase__")
# 	await add_qt(m.chat.id)
# 	await x.edit("__Chat has been added to DataBase\nFrom now you will get daily quotes__")

# @Client.on_message(filters.command(["del_qt"]))
# @error_handler
# async def qt_remove(c, m):
# 	x = await m.reply_text("__Removing Chat from DataBase__")
# 	await del_qt(m.chat.id)
# 	await x.edit("__Chat has been removed from DataBase\nFrom now you won't get daily quotes__")

@Client.on_message(filters.command(["weeb", "weebify"]))
@error_handler
async def weebify(c, m):
    wb = await m.reply_text("`Wi8...`")
    args = None
    try:
        args = m.text.split(None, 1)[1]
    except IndexError:
       if m.reply_to_message:
         args = m.reply_to_message.text
       else:
         None
    if not args:
        await wb.edit("`What I am Supposed to Weebify U Dumb`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await wb.edit(string)

@Client.on_message(filters.command("send"))
@error_handler
async def send_msg(c,m):
    try:
       text = m.text.split(None, 1)[1]
    except IndexError:
      text=None
    if text:
       await c.send_message(m.chat.id, text)
    elif m.reply_to_message:
       await m.reply_to_message.copy(m.chat.id)

@Client.on_message(filters.command(['emoji']))
@error_handler
async def emoji(client, message):
    op = await message.reply_text("`Emojifying the text..`")
    try:
      args = message.text.split(None, 1)[1]
    except IndexError:
      args = None
    if not args:
        if not message.reply_to_message:
           try:
               return await op.edit("__What am I Supposed to do with this idiot, Give me a text.__")
           except Exception as e:
               print(f"Error editing message in emoji: {e}")
        if not message.reply_to_message.text:
           try:
               return await op.edit("__What am I Supposed to do with this idiot, Give me a text.__")
           except Exception as e:
               print(f"Error editing message in emoji: {e}")
    args = args or message.reply_to_message.text
    
    result = ""
    for a in args:
        a = a.lower()
        if a in kakashitext:
            char = kakashiemoji[kakashitext.index(a)]
            result += char
        else:
            result += a
    try:
        await op.edit(result)
    except Exception as e:
        print(f"Error editing message in emoji: {e}")
    
    

@Client.on_message(filters.command(['cmoji']))
@error_handler
async def c_emoji(client, message):
    ok = await message.reply_text("`Emojifying the text..`")
    try:
      args = message.text.split(None, 1)[1]
    except IndexError:
      args = None
    if not args:
        if not message.reply_to_message:
           try:
               return await ok.edit("__What am I Supposed to do with this idiot, Give me a text.__")
           except Exception as e:
               print(f"Error editing message in c_emoji: {e}")
        if not message.reply_to_message.text:
           try:
               return await ok.edit("__What am I Supposed to do with this idiot, Give me a text.__")
           except Exception as e:
               print(f"Error editing message in c_emoji: {e}")
    args = args or message.reply_to_message.text
    try:
        emoji, arg = args.split(" ", 1)
    except Exception:
        arg = args
        emoji = "😎"
    result = ""
    for a in arg:
        a = a.lower()
        if a in kakashitext:
            char = itachiemoji[kakashitext.index(a)].format(cj=emoji)
            result += char
        else:
            result += a
    await ok.edit(result)

@Client.on_message(filters.command(["ftext", "f"]))
@error_handler
async def ftext(client, message):
    try:
        input_str = message.text.split(None, 1)[1]
    except IndexError:
        input_str = None
    if input_str:
        paytext = input_str
        pay = "{}{}{}{}{}{}{}{}{}{}".format(
            paytext * 8,
            paytext * 8,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 6,
            paytext * 6,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 2,
        )
    else:
        pay = "╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯\n"
    try:
        if message.reply_to_message:
            await message.reply_to_message.reply_text(pay)
        else:
            await message.reply_text(pay)
    except Exception as e:
        print(f"Error sending message in ftext: {e}")

@Client.on_message(filters.command(["ytc"]))
@error_handler
async def yt_comment(client, message):
   ytc = await message.reply_text("`Making Comment`")
   try:
        input_str = message.text.split(None, 1)[1]
   except IndexError:
        await ytc.edit("`Gib Some text to Make yt comment, U Dumb!`")
        return
   text = urllib.parse.quote_plus(input_str)
   name0 = message.from_user.first_name
   name = urllib.parse.quote_plus(name0)
   img = None
   pic = None
   try:
       async for photo in client.get_chat_photos(message.from_user.id, limit=1):
          img = photo 
       if img:
           pic = await client.download_media(img.file_id)
       else:
           # Fallback if no profile photo is found, use a default avatar or handle as error
           raise ValueError("No profile photo found.")

       kk = upload_file(pic)
       imglink = f"https://telegra.ph{kk[0]}"
       lol = f"https://some-random-api.com/canvas/youtube-comment?avatar={imglink}&username={name}&comment={text}"
      # await ytc.edit(lol)
       await client.send_photo(message.chat.id, lol, caption=f"__**Made using @Mr_StarkBot**__")
   except Exception as e:
       print(f"Error in yt_comment: {e}")
       try:
           await ytc.edit(f"Error making YouTube comment: {e}")
       except Exception as edit_e:
           print(f"Error editing message after yt_comment failure: {edit_e}")
   finally:
       if pic and os.path.exists(pic):
           os.remove(pic)
       try:
           await ytc.delete()
       except Exception as delete_e:
           print(f"Error deleting message in yt_comment finally block: {delete_e}")

@Client.on_message(filters.command(["rytc"]))
@error_handler
async def ryt_comment(client, message):
     ytc = await message.reply_text("`Making Comment`")
     try:
          input_str = message.text.split(None, 1)[1]
     except IndexError:
          await ytc.edit("`Gib Some text to Make yt comment, U Dumb!`")
          return
     text = urllib.parse.quote_plus(input_str)
     name0 = message.from_user.first_name
     name = urllib.parse.quote_plus(name0)
     link = random.choice(AVATARS)    
     lol = f"https://some-random-api.com/canvas/youtube-comment?avatar={link}&username={name}&comment={text}"
   #  await ytc.edit(lol)
     await client.send_photo(message.chat.id, lol, caption=f"__**Made using @Mr_StarkBot**__")
     await ytc.delete()

@Client.on_message(filters.command(["quotly"]))
@error_handler
async def quotly(client, message):
    try:
        if not message.reply_to_message:
            return await message.reply_text("Reply to a message to quotly it.")
        if not message.reply_to_message.text:
            return await message.reply_text("Reply to a text message to quotly it.")

        quote = message.reply_to_message.text
        user = message.reply_to_message.from_user.first_name
        chat = message.reply_to_message.chat.title
        pic = None
        try:
            async for photo in client.get_chat_photos(message.reply_to_message.from_user.id, limit=1):
                pic = await client.download_media(photo.file_id)
        except Exception as e:
            print(f"Error downloading user photo for quotly: {e}")
            # Continue without a profile picture if download fails

        data = {
            "type": "quote",
            "format": "png",
            "backgroundColor": "#1b1429",
            "width": 512,
            "height": 768,
            "scale": 2,
            "messages": [
                {
                    "entities": [],
                    "avatar": True,
                    "from": {
                        "id": 1,
                        "name": user,
                        "photo": {
                            "url": pic if pic else ""
                        }
                    },
                    "text": quote,
                    "replyMessage": {}
                }
            ]
        }

        if chat:
            data["messages"][0]["from"]["name"] = f"{user} in {chat}"

        headers = {'Content-Type': 'application/json'}
        url = "https://bot.lyo.su/quote/generate"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    await message.reply_photo(BytesIO(image_data))
                else:
                    error_message = await resp.text()
                    await message.reply_text(f"Error generating quote: {error_message}")
    except Exception as e:
        print(f"Error in quotly function: {e}")
        await message.reply_text(f"An unexpected error occurred: {e}")
    finally:
        if pic and os.path.exists(pic):
            os.remove(pic)


@Client.on_message(filters.command(["write"]))
@error_handler
async def weebify(c, m):
    wb = await m.reply_text("`Wi8...`")
    args = None
    try:
        args = m.text.split(None, 1)[1]
    except IndexError:
       if m.reply_to_message:
         args = m.reply_to_message.text
       else:
         None
    if not args:
        await wb.edit("`What I am Supposed to Weebify U Dumb`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await wb.edit(string)

@Client.on_message(filters.command("send"))
@error_handler
async def send_msg(c,m):
    try:
       text = m.text.split(None, 1)[1]
    except IndexError:
      text=None
    if text:
       await c.send_message(m.chat.id, text)
    elif m.reply_to_message:
       await m.reply_to_message.copy(m.chat.id)

@Client.on_message(filters.command(['emoji']))
@error_handler
async def emoji(client, message):
    op = await message.reply_text("`Emojifying the text..`")
    try:
      args = message.text.split(None, 1)[1]
    except IndexError:
      args = None
    if not args:
        if not message.reply_to_message:
           try:
               return await op.edit("__What am I Supposed to do with this idiot, Give me a text.__")
           except Exception as e:
               print(f"Error editing message in emoji: {e}")
        if not message.reply_to_message.text:
           try:
               return await op.edit("__What am I Supposed to do with this idiot, Give me a text.__")
           except Exception as e:
               print(f"Error editing message in emoji: {e}")
    args = args or message.reply_to_message.text
    
    result = ""
    for a in args:
        a = a.lower()
        if a in kakashitext:
            char = kakashiemoji[kakashitext.index(a)]
            result += char
        else:
            result += a
    try:
        await op.edit(result)
    except Exception as e:
        print(f"Error editing message in emoji: {e}")