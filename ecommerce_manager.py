#!/usr/bin/env python3
"""
电商运营管理平台 - 基础版本
适用于京东、淘宝等电商平台的数据分析和管理
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import time

class EcommerceManager:
    def __init__(self):
        self.init_session_state()
        
    def init_session_state(self):
        """初始化会话状态"""
        if 'sales_data' not in st.session_state:
            st.session_state.sales_data = pd.DataFrame()
        if 'products' not in st.session_state:
            st.session_state.products = pd.DataFrame()
        if 'inventory' not in st.session_state:
            st.session_state.inventory = pd.DataFrame()
    
    def load_sample_data(self):
        """加载示例数据"""
        # 销售数据
        sales_dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        sales_data = pd.DataFrame({
            'date': sales_dates,
            'sales_amount': [1000 + i*10 + (i%7)*100 for i in range(len(sales_dates))],
            'order_count': [20 + i*0.5 + (i%7)*5 for i in range(len(sales_dates))],
            'platform': ['京东' if i%2==0 else '淘宝' for i in range(len(sales_dates))]
        })
        
        # 产品数据
        products = pd.DataFrame({
            'product_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
            'product_name': ['无线鼠标', '机械键盘', 'USB集线器', '笔记本支架', '摄像头'],
            'category': ['外设', '外设', '配件', '配件', '外设'],
            'price': [99, 299, 49, 89, 199],
            'stock': [150, 80, 200, 120, 60],
            'sales_7d': [25, 15, 40, 18, 12]
        })
        
        st.session_state.sales_data = sales_data
        st.session_state.products = products
        st.session_state.inventory = products[['product_id', 'product_name', 'stock']]
    
    def dashboard_page(self):
        """仪表板页面"""
        st.title("📊 电商运营仪表板")
        
        if st.button("加载示例数据"):
            self.load_sample_data()
        
        if st.session_state.sales_data.empty:
            st.warning("请先加载数据")
            return
        
        # 关键指标
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sales = st.session_state.sales_data['sales_amount'].sum()
            st.metric("总销售额", f"¥{total_sales:,.0f}")
        
        with col2:
            total_orders = st.session_state.sales_data['order_count'].sum()
            st.metric("总订单数", f"{total_orders:,.0f}")
        
        with col3:
            avg_order_value = total_sales / total_orders if total_orders > 0 else 0
            st.metric("客单价", f"¥{avg_order_value:.2f}")
        
        with col4:
            low_stock = len(st.session_state.products[st.session_state.products['stock'] < 50])
            st.metric("低库存商品", low_stock)
        
        # 销售趋势图
        st.subheader("销售趋势")
        fig_sales = px.line(
            st.session_state.sales_data, 
            x='date', 
            y='sales_amount',
            color='platform',
            title="销售额趋势"
        )
        st.plotly_chart(fig_sales, use_container_width=True)
        
        # 产品分析
        st.subheader("产品分析")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_category = px.pie(
                st.session_state.products,
                values='sales_7d',
                names='category',
                title="各类别销售占比"
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
        with col2:
            top_products = st.session_state.products.nlargest(5, 'sales_7d')
            fig_top = px.bar(
                top_products,
                x='product_name',
                y='sales_7d',
                title="热销商品TOP5"
            )
            st.plotly_chart(fig_top, use_container_width=True)
    
    def inventory_page(self):
        """库存管理页面"""
        st.title("📦 库存管理")
        
        if st.session_state.products.empty:
            st.warning("请先加载数据")
            return
        
        # 库存预警
        low_stock = st.session_state.products[st.session_state.products['stock'] < 50]
        if not low_stock.empty:
            st.error("⚠️ 库存预警商品:")
            for _, product in low_stock.iterrows():
                st.write(f"- {product['product_name']}: 库存 {product['stock']}")
        
        # 库存表格
        st.subheader("库存详情")
        inventory_display = st.session_state.products.copy()
        inventory_display['库存状态'] = inventory_display['stock'].apply(
            lambda x: '充足' if x >= 100 else ('偏低' if x >= 50 else '紧急')
        )
        st.dataframe(inventory_display, use_container_width=True)
        
        # 补货建议
        st.subheader("智能补货建议")
        for _, product in st.session_state.products.iterrows():
            daily_sales = product['sales_7d'] / 7
            days_of_stock = product['stock'] / daily_sales if daily_sales > 0 else 999
            
            if days_of_stock < 7:
                suggest_qty = int(daily_sales * 30 - product['stock'])
                st.write(f"🔄 {product['product_name']}: 建议补货 {suggest_qty} 件 (当前库存可用 {days_of_stock:.1f} 天)")
    
    def price_monitor_page(self):
        """价格监控页面"""
        st.title("💰 价格监控")
        
        st.write("功能开发中...")
        st.write("计划功能:")
        st.write("- 竞品价格追踪")
        st.write("- 历史价格分析") 
        st.write("- 价格变动预警")
        st.write("- 自动调价建议")
        
        # 示例价格数据
        price_data = pd.DataFrame({
            'product': ['无线鼠标', '机械键盘', 'USB集线器'],
            'our_price': [99, 299, 49],
            'competitor_avg': [109, 279, 59],
            'price_advantage': ['低10元', '高20元', '低10元']
        })
        st.dataframe(price_data, use_container_width=True)
    
    def reports_page(self):
        """报表生成页面"""
        st.title("📈 运营报表")
        
        if st.session_state.sales_data.empty:
            st.warning("请先加载数据")
            return
        
        # 时间范围选择
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("开始日期", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("结束日期", datetime.now())
        
        # 生成报表
        if st.button("生成报表"):
            filtered_data = st.session_state.sales_data[
                (st.session_state.sales_data['date'].dt.date >= start_date) &
                (st.session_state.sales_data['date'].dt.date <= end_date)
            ]
            
            if not filtered_data.empty:
                st.subheader(f"{start_date} 至 {end_date} 销售报表")
                
                # 汇总数据
                total_sales = filtered_data['sales_amount'].sum()
                total_orders = filtered_data['order_count'].sum()
                avg_daily_sales = total_sales / len(filtered_data)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("总销售额", f"¥{total_sales:,.0f}")
                with col2:
                    st.metric("总订单数", f"{total_orders:,.0f}")
                with col3:
                    st.metric("日均销售额", f"¥{avg_daily_sales:.0f}")
                
                # 详细数据表格
                st.subheader("详细数据")
                st.dataframe(filtered_data, use_container_width=True)
                
                # 导出按钮
                csv_data = filtered_data.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    "下载CSV报表",
                    csv_data,
                    f"sales_report_{start_date}_{end_date}.csv",
                    "text/csv"
                )
    
    def run(self):
        """运行应用"""
        st.set_page_config(
            page_title="电商运营管理平台",
            page_icon="🏪",
            layout="wide"
        )
        
        # 侧边栏导航
        st.sidebar.title("功能导航")
        page = st.sidebar.selectbox(
            "选择功能",
            ["仪表板", "库存管理", "价格监控", "运营报表"]
        )
        
        # 页面路由
        if page == "仪表板":
            self.dashboard_page()
        elif page == "库存管理":
            self.inventory_page()
        elif page == "价格监控":
            self.price_monitor_page()
        elif page == "运营报表":
            self.reports_page()
        
        # 侧边栏信息
        st.sidebar.markdown("---")
        st.sidebar.info("版本: 1.0.0")
        st.sidebar.info("作者: AI助手")

if __name__ == "__main__":
    app = EcommerceManager()
    app.run()